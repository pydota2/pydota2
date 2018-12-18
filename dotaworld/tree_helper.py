###
### Helper Class/Funcs for dealing with Trees
###

import json

BOUNDING_SIZE   = 64.
BOUNDING_OFFSET = BOUNDING_SIZE / 2.

class Dota2_Tree:
    def __init__(self, id, x, y, z):
        self.id     = id
        self.x      = x
        self.y      = y
        self.z      = z
        self.alive  = True

    def getBoundingBox(self):
        return (self.x-BOUNDING_OFFSET, self.y+BOUNDING_OFFSET), \
               (self.x+BOUNDING_OFFSET, self.y-BOUNDING_OFFSET)

    def destroy(self):
        self.alive = False
        #print('Destroyed', self)

    def respawn(self):
        self.alive = True
        #print('Respawned', self)

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, indent=2)

    def __str__(self):
        return self.toJSON()

    def __repr__(self):
        return json.dumps(self, default=lambda o: o.__dict__)


class Dota2_Trees:
    def __init__(self):
        self.tree_list = dict()

    def destroyTrees(self, ids=[]):
        [self.tree_list[id].destroy() for id in ids]

    def respawnTrees(self, ids=[]):
        [self.tree_list[id].respawn() for id in ids]

    def getTreesInBoundingBox(self, x1, y1, x2, y2, aliveOnly=True):
        ret = []
        for t in self.tree_list.values():
            if t.x >= min(x1,x2) and t.x <= max(x1,x2) \
                and t.y >= min(y1,y2) and t.y <= max(y1,y2):
                if aliveOnly and t.alive:
                    #ret.append(t)
                    ret.append(t.id)
                elif not aliveOnly:
                    #ret.append(t)
                    ret.append(t.id)
        return ret

    def _loadTrees(self, filename):
        with open(filename, 'r') as fh:
            lines = fh.readlines()
            for line in lines:
                tree_id, x, y, z = line.split()
                tree_id = int(tree_id)
                x = int(x)
                y = int(y)
                z = int(z)
                if x != 0 and y != 0 and z != 0:
                    self.tree_list[tree_id] = Dota2_Tree(tree_id, x, y, z)

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, indent=2)


if __name__ == "__main__":
    trees = Dota2_Trees()
    trees._loadTrees("patching/tree.data")
    print(trees.getTreesInBoundingBox(-7000, -5440, 7000, -5340))
    trees.destroyTrees([588,589,590])
    print(trees.getTreesInBoundingBox(-7000, -5440, 7000, -5340))
    #print(trees.toJSON())