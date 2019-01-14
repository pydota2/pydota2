#!/bin/bash

#if [ "$(uname)" == "Darwin" ]; then
#    brew install rabbitmq
#    /usr/local/opt/rabbitmq/sbin/rabbitmq-plugins enable rabbitmq_recent_history_exchange
#elif [ "$(expr substr $(uname -s) 1 5)" == "Linux" ]; then
#    sudo apt-get install rabbitmq
#fi

# build dotaservice egg
cd dotaservice
pip3 install -e .
cd ..

# build dotaworld egg
cd dotaworld
pip3 install -e .
cd ..

# build pydota2 egg
pip3 install -e .
