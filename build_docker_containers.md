To install appropriate Docker containers, please do the following:

cd dotaservice

# build Dota2
sudo docker build -t dota . -f docker/Dockerfile-dota --build-arg user=$STEAM_ID --build-arg pwd=$STEAM_PWD --build-arg guard=

# If "Account Logon Denied"
# Check your authenticator (phone) and append the appropriate code (e.g. ABC123) and rerun

# build DotaService
sudo docker build -t dotaservice . -f docker/Dockerfile-dotaservice

cd ..
