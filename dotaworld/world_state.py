###
### Helper file for Dota2 Entity/World Event representation
### - expose world data in a more useful form than the raw protos
###

from dotaservice.protos.dota_gcmessages_common_bot_script_pb2 import CMsgBotWorldState

from os.path import join
import math
import collections
import location as loc
import json


def load_json_file(fname):
    fname = join('patching', fname)
    with open(fname, 'r') as infile:
        return json.load(infile)


"""
THIS FILE IS NOT COMPLETE ALTHOUGH IT WILL COMPILE
THIS IS A WORK-IN-PROGRESS 
"""

ability_data = None
hero_data = None
unit_data = None

class HeroSelectionData(object):
    """Handle initial data durning hero selection."""

    def __init__(self, data):
        """Takes data from Valve provided JSON-like text files."""
        # make sure we are in hero selection
        assert data.game_state == 3
        self.data = data


class AbilityData(object):
    """Maintain certain information about abilities."""
    def __init__(self, id, data):
        self.ability_id = id
        self.data = data

    def get_name(self):
        return ability_data[str(self.ability_id)]['Name']

    def get_level(self):
        return self.data.level

    def get_cast_range(self):
        return self.data.cast_range

    def get_cd_remaining(self):
        return self.data.cooldown_remaining

    def get_channel_time(self):
        return self.data.channel_time

    def is_channeling(self):
        return self.data.is_channeling

    def is_hidden(self):
        return 'Hidden' in ability_data[str(self.ability_id)].keys()

    def is_ultimate(self):
        return 'Ultimate' in ability_data[str(self.ability_id)].keys()

    def is_talent(self):
        return 'Talent' in ability_data[str(self.ability_id)].keys()

    def get_ult_starting_level(self):
        if 'LevelAvailable' in ability_data[str(self.ability_id)].keys():
            return ability_data[str(self.ability_id)]['LevelAvailable']
        else:
            return 6

    def get_ult_level_interval(self):
        if 'LevelsBetweenUpgrades' in ability_data[str(self.ability_id)].keys():
            return ability_data[str(self.ability_id)]['LevelsBetweenUpgrades']
        else:
            return 6

    def __str__(self):
        ret  = "<AbilityData>\n"
        ret += "\tName: %s\n" % (self.get_name())
        ret += "\tLevel: %d\n" % (self.get_level())
        return ret


# NOTE: Items are "abilities" in all respects in Dota2
class ItemData(object):
    """Maintain certain information about items."""
    def __init__(self, id, data):
        self.item_id = id
        self.data = data

    def get_name(self):
        return ability_data[str(self.item_id)]['Name']

    def get_charges(self):
        return self.data.charges

    def get_secondary_charges(self):
        return self.data.secondary_charges

    def get_power_treads_stat(self):
        return self.data.power_treads_stat

    def __str__(self):
        ret  = "<ItemData>\n"
        ret += "\tName: %s\n" % self.get_name()
        return ret


class ModifierData(object):
    """Maintain certain information about modifiers."""
    def __init__(self, data):
        self.data = data

    def get_name(self):
        return self.data.name

    def get_ability_id(self):
        return self.data.ability_id

    def get_stack_count(self):
        return self.data.stack_count

    def get_remaining_duration(self):
        return self.data.remaining_duration

    def __str__(self):
        ret  = "<ModifierData>\n"
        ret += "\tName: %s\n" % self.get_name()
        return ret


class UnitData(object):
    """Maintain certain information about units."""
    def __init__(self, handle, data):
        self.handle = handle
        self.data = data

    def get_name(self):
        return self.data.name

    def get_type(self):
        return self.data.unit_type

    def get_level(self):
        return self.data.level

    def get_location(self):
        return loc.Location.build(self.data.location)

    def is_alive(self):
        return self.data.is_alive

    def get_facing(self):
        return self.data.facing

    def get_health(self):
        return self.data.health

    def get_max_health(self):
        return self.data.health_max

    def get_health_regen(self):
        return self.data.health_regen

    def get_mana(self):
        return self.data.mana

    def get_max_mana(self):
        return self.data.mana_max

    def get_mana_regen(self):
        return self.data.mana_regen

    def get_anim_activity(self):
        return self.data.anim_activity

    def get_curr_move_speed(self):
        return self.data.current_movement_speed

    def is_stunned(self):
        return self.data.is_stunned

    def is_rooted(self):
        return self.data.is_rooted

    def get_xp_needed_to_level(self):
        return self.data.xp_needed_to_level

    def get_net_worth(self):
        return self.data.net_worth

    def __str__(self):
        ret  = "<UnitData>\n"
        ret += "\tName: %s\n" % self.get_name()
        return ret


class PlayerData(object):
    """Maintain certain information about our players."""
    def __init__(self, time, pID, heroID):
        self.pid = pID
        self.hero_id = heroID
        self.prtt = collections.deque(maxlen=10)
        self.avg_prtt = 0.3 #TODO (nostrademous) Fix this to frame rate
        self.abilities = []
        self.items = []
        self.modifiers = []

        self.prev_time  = time
        self.prev_pdata = None
        self.prev_udata = None
        self.curr_time  = time
        self.pdata = None
        self.udata = None

    def save_last_update(self, time, udata, pdata):
        self.prev_time = self.curr_time
        self.prev_pdata = self.pdata
        self.prev_udata = self.udata

        self.curr_time = time
        self.pdata = pdata
        self.udata = udata
        self.update_abilities()
        self.update_items()
        self.update_modifiers()

        self._update_prtt()

    def get_name(self):
        return hero_data[str(self.hero_id)]['Name']

    def get_time_since_last_seen(self):
        return self.curr_time - self.prev_time

    def get_talent_choice(self, tier):
        if 'Talents' in hero_data[str(self.hero_id)].keys():
            talents = hero_data[str(self.hero_id)]['Talents']
            tier = (tier-1)*2+1
            return talents['Talent_'+str(tier)], talents['Talent_'+str(tier+1)]
        else:
            return None, None

    # track player round trip time (prtt)
    def _update_prtt(self):
        time_delta = self.get_time_since_last_seen()
        # TODO - (nostrademous) if game is paused, does game_time increment?
        # I know, dota_time doesn't. Anyways, only update avg prtt when delta
        # is greater than 0
        if time_delta > 0.:
            self.prtt.append(time_delta)
            self.avg_prtt = sum(self.prtt)/float(len(self.prtt))

    def is_alive(self):
        return self.pdata.is_alive

    def get_anim_activity(self):
        return self.udata.get_anim_activity()

    def get_location(self):
        return self.udata.get_location()

    def get_movement_vector(self):
        if self.prev_udata:
            return self.get_location() - loc.Location.build(self.prev_udata.location)
        return loc.center

    def get_location_xyz(self):
        l = self.get_location()
        return l.x, l.y, l.z

    def get_turn_rate(self):
        if 'TurnRate' in hero_data[str(self.hero_id)].keys():
            return hero_data[str(self.hero_id)]['TurnRate']
        else:
            print('<ERROR>: Missing TurnRate for pID: %d' % self.hero_id)
            return 0.5

    def time_to_face_heading(self, heading):
        # we want a facing differential between 180 and -180 degrees
        # since we will always turn in the direction of smaller angle,
        # never more than a 180 degree turn
        diff = math.fabs(heading - self.udata.get_facing())
        if diff > 180.0:
            diff = math.fabs(360.0 - diff)
        time_to_turn_180 = 0.03*math.pi/self.get_turn_rate()
        #print("[%d] Facing: %f, Heading: %f, Diff: %f, TurnTime180: %f, TimeToTurn: %f" %
        #     (self.pid, self.udata.data.facing, heading, diff, time_to_turn_180, (diff/180.0)*time_to_turn_180))
        return (diff/180.0)*time_to_turn_180

    def time_to_face_location(self, location):
        loc_delta = loc.Location.build(location) - self.get_location()
        desired_heading = math.degrees(math.atan2(loc_delta.y, loc_delta.x))
        return self.time_to_face_heading(desired_heading)

    def get_reachable_distance(self, time_adj=0.0):
        currSpd = self.udata.get_curr_move_speed()
        timeAvail = self.avg_prtt - time_adj
        dist = timeAvail * currSpd
        #print("[%d] Speed: %f, TimeAvail: %f, Reachable Distance: %f" %
        #     (self.pid, currSpd, timeAvail, dist))
        return dist

    def max_reachable_location(self, heading):
        ttfh = self.time_to_face_heading(heading)
        max_reachable_dist = self.get_reachable_distance(ttfh)
        rad_angle = math.pi/2.0 - math.radians(heading)
        l = self.get_location()
        retLoc = loc.Location(l.x + 5.0*max_reachable_dist*math.cos(rad_angle),
                              l.y + 5.0*max_reachable_dist*math.sin(rad_angle),
                              l.z)
        return retLoc

    def update_abilities(self):
        self.abilities = []
        for ab in self.udata.data.abilities:
            self.abilities.append(AbilityData(ab.ability_id, ab))

    def update_items(self):
        self.items = []
        for item in self.udata.data.items:
            self.items.append(ItemData(item.ability_id, item))

    def update_modifiers(self):
        self.modifiers = []
        for mod in self.udata.data.modifiers:
            self.modifiers.append(ModifierData(mod))

    def get_abilities(self):
        return self.abilities

    def get_ability_points(self):
        return self.udata.data.ability_points

    def get_level(self):
        return self.udata.data.level

    def get_items(self):
        return self.items

    def get_modifiers(self):
        return self.modifiers

    def get_is_stunned(self):
        return self.udata.is_stunned()

    def get_is_rooted(self):
        return self.udata.is_rooted()

    def __str__(self):
        ret  = "<PlayerData>\n"
        ret += "\tName: %s\n" % self.get_name()
        for ability in self.get_abilities():
            ret += str(ability)
        for item in self.get_items():
            ret += str(item)
        for mod in self.get_modifiers():
            ret += str(mod)
        return ret


class WorldData(object):
    """Expose world data in a more useful form than the raw protos."""

    def __init__(self, data):
        global ability_data, hero_data, unit_data
        """Takes data from Valve provided JSON-like text files."""
        # make sure we are in game
        assert data.game_state in [4,5]

        ability_data = load_json_file('abilities.json')
        hero_data = load_json_file('heroes.json')
        unit_data = load_json_file('units.json')

        self.team_id = data.team_id
        self.game_state = data.game_state
        self.player_data = {}
        self.update_time = data.game_time

        self._create_units(data.units)
        self._update_players(data.players)

        for player_id in self.good_players.keys():
            self.player_data[player_id] = PlayerData(data.game_time, player_id,
                self.good_players[player_id]['player'].hero_id)
            self.player_data[player_id].save_last_update(data.game_time,
                                                         self.good_players[player_id]['unit'],
                                                         self.good_players[player_id]['player'])

        # initialization of various unit-handle lookup lists

        self.good_ancient = None
        self.bad_ancient = None

        self.good_courier = None
        self.bad_courier = None

        self.roshan = None

    def update_world_data(self, data):
        # make sure we are in game
        assert data.game_state in [4,5]

        self.game_state = data.game_state
        self.update_delta = data.game_time - self.update_time
        self.update_time = data.game_time
        self._create_units(data.units)
        self._update_players(data.players)

        for player_id in self.good_players.keys():
            if not player_id in self.player_data.keys():
                self.player_data[player_id] = PlayerData(player_id,
                    self.good_players[player_id]['player'].hero_id)
            self.player_data[player_id].save_last_update(data.game_time,
                                                         self.good_players[player_id]['unit'],
                                                         self.good_players[player_id]['player'])

    def _create_units(self, unit_data):
        self.good_players = {}  # on my team
        self.bad_players = {}   # on enemy team

        self.units = {}

        self.good_hero_units = []
        self.bad_hero_units = []

        self.good_lane_creep = []
        self.bad_lane_creep = []

        self.jungle_creep = []

        self.good_towers = []
        self.bad_towers = []

        self.good_rax = []
        self.bad_rax = []

        self.good_shrines = []
        self.bad_shrines = []

        self.good_wards = []
        self.bad_wards = []

        # buildings == effigies
        self.good_buildings = []
        self.bad_buildings = []

        bInvalidFound = False
        for unit in unit_data:
            self.units[unit.handle] = UnitData(unit.handle, unit)

            if unit.unit_type == CMsgBotWorldState.UnitType.Value('HERO'):
                if unit.team_id == self.team_id:
                    self.good_players[unit.player_id] = {'unit': self.units[unit.handle]}
                else:
                    self.bad_players[unit.player_id] = {'unit': self.units[unit.handle]}

            elif unit.unit_type == CMsgBotWorldState.UnitType.Value('CREEP_HERO'):
                if unit.team_id == self.team_id:
                    self.good_hero_units.append(unit.handle)
                else:
                    self.bad_hero_units.append(unit.handle)

            elif unit.unit_type == CMsgBotWorldState.UnitType.Value('LANE_CREEP'):
                if unit.team_id == self.team_id:
                    self.good_lane_creep.append(self.units[unit.handle])
                else:
                    self.bad_lane_creep.append(self.units[unit.handle])

            elif unit.unit_type == CMsgBotWorldState.UnitType.Value('JUNGLE_CREEP'):
                self.jungle_creep.append(self.units[unit.handle])

            elif unit.unit_type == CMsgBotWorldState.UnitType.Value('ROSHAN'):
                self.roshan = self.units[unit.handle]

            elif unit.unit_type == CMsgBotWorldState.UnitType.Value('TOWER'):
                if unit.team_id == self.team_id:
                    self.good_towers.append(self.units[unit.handle])
                else:
                    self.bad_towers.append(self.units[unit.handle])

            elif unit.unit_type == CMsgBotWorldState.UnitType.Value('BARRACKS'):
                if unit.team_id == self.team_id:
                    self.good_rax.append(self.units[unit.handle])
                else:
                    self.bad_rax.append(self.units[unit.handle])

            elif unit.unit_type == CMsgBotWorldState.UnitType.Value('SHRINE'):
                if unit.team_id == self.team_id:
                    self.good_shrines.append(self.units[unit.handle])
                else:
                    self.bad_shrines.append(self.units[unit.handle])

            # ANCIENT
            elif unit.unit_type == CMsgBotWorldState.UnitType.Value('FORT'):
                if unit.team_id == self.team_id:
                    self.good_ancient = self.units[unit.handle]
                else:
                    self.bad_ancient = self.units[unit.handle]

            elif unit.unit_type == CMsgBotWorldState.UnitType.Value('BUILDING'):
                if unit.team_id == self.team_id:
                    self.good_buildings = self.units[unit.handle]
                else:
                    self.bad_buildings= self.units[unit.handle]

            elif unit.unit_type == CMsgBotWorldState.UnitType.Value('COURIER'):
                if unit.team_id == self.team_id:
                    self.good_courier = self.units[unit.handle]
                else:
                    self.bad_courier = self.units[unit.handle]

            elif unit.unit_type == CMsgBotWorldState.UnitType.Value('WARD'):
                if unit.team_id == self.team_id:
                    self.good_wards = self.units[unit.handle]
                else:
                    self.bad_wards = self.units[unit.handle]

            elif unit.unit_type == CMsgBotWorldState.UnitType.Value('INVALID'):
                #print("INVALID UNIT TYPE:\n%s" % str(unit))
                bInvalidFound = True

    def _update_players(self, player_data):
        for player in player_data:
            if player.player_id in self.good_players.keys():
                self.good_players[player.player_id]['player'] = player
            elif player.player_id in self.bad_players.keys():
                self.bad_players[player.player_id]['player'] = player

    def get_available_level_points(self, player_id):
        player = self.get_player_by_id(player_id)
        if player:
            return player.get_ability_points()
        return 0

    def get_unit_by_handle(self, unit_data, handle):
        for unit in unit_data:
            if unit.handle == handle:
                return unit
        return None

    def get_player_by_id(self, player_id):
        if player_id in self.player_data.keys():
            return self.player_data[player_id]
        return None

    def get_player_abilities(self, player_id):
        player = self.get_player_by_id(player_id)
        if player:
            return player.get_abilities()
        return []

    # this returns only ability IDs of abilties that can be leveled
    def get_player_ability_ids(self, player_id, bCanBeLeveled=True):
        if self.get_available_level_points(player_id) == 0:
            return []

        player = self.get_player_by_id(player_id)
        abilities = self.get_player_abilities(player_id)

        p_level = player.get_level()

        ids = []
        a_ids = []
        for ability in abilities:
            id = ability.ability_id
            a_ids.append(ability.get_name())

            # generic_hidden
            if id == 6251:
                continue

            # if we are considering level-based restrictions
            if bCanBeLeveled:

                # skip hidden abilities
                if ability.is_hidden():
                    continue

                # skip talents here
                if ability.is_talent():
                    continue

                a_level = ability.get_level()

                if a_level >= int(float(p_level/2.0)+0.5):
                    continue

                if ability.is_ultimate():
                    # can't level ultimate past 3 levels
                    if a_level >= 3:
                        continue

                    start_level = ability.get_ult_starting_level()
                    level_interval = ability.get_ult_level_interval()
                    if p_level < start_level:
                        continue
                    if p_level < (start_level + (a_level * level_interval)):
                        continue
                else:
                    # can't level abilities past 4 levels (invoker exception)
                    if a_level >= 4:
                        continue

            # if we get here it can be leveled or we didn't care
            ids.append(ability.get_name())

        t1_talent_picked = False
        if p_level >= 10:
            choice_1, choice_2 = player.get_talent_choice(1)
            if (not choice_1 in a_ids) and (not choice_2 in a_ids):
                ids.append(choice_1)
                ids.append(choice_2)
            else:
                t1_talent_picked = True

        t2_talent_picked = False
        if p_level >= 15 and t1_talent_picked:
            choice_1, choice_2 = player.get_talent_choice(2)
            if (not choice_1 in a_ids) and (not choice_2 in a_ids):
                ids.append(choice_1)
                ids.append(choice_2)
            else:
                t2_talent_picked = True

        t3_talent_picked = False
        if p_level >= 20 and t2_talent_picked:
            choice_1, choice_2 = player.get_talent_choice(3)
            if (not choice_1 in a_ids) and (not choice_2 in a_ids):
                ids.append(choice_1)
                ids.append(choice_2)
            else:
                t3_talent_picked = True

        t4_talent_picked = False
        if p_level >= 25 and t3_talent_picked:
            choice_1, choice_2 = player.get_talent_choice(4)
            if (not choice_1 in a_ids) and (not choice_2 in a_ids):
                ids.append(choice_1)
                ids.append(choice_2)
            else:
                t4_talent_picked = True

        return ids

    def is_player_alive(self, player_id):
        player = self.get_player_by_id(player_id)
        if player:
            return player.is_alive()
        return False

    def is_player_stunned(self, player_id):
        player = self.get_player_by_id(player_id)
        if player:
            return player.get_is_stunned()
        return False

    def is_player_rooted(self, player_id):
        player = self.get_player_by_id(player_id)
        if player:
            return player.get_is_rooted()
        return False

    def get_player_items(self, player_id):
        player = self.get_player_by_id(player_id)
        if player:
            return player.get_items()
        return []

    def get_unit_location(self, unit):
        return loc.Location.build(unit.location)

    def get_player_location(self, player_id):
        player = self.get_player_by_id(player_id)
        if player:
            return player.get_location()
        return loc.center

    def get_player_ids(self):
        return list(self.player_data.keys())

    @property
    def get_my_players(self):
        return self.good_players

    @property
    def get_my_minions(self):
        return self.good_hero_units
