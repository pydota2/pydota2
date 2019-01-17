#!/bin/bash

# Install RabbitMQ
if [ "$(uname)" == "Darwin" ]; then
    brew install rabbitmq
    /usr/local/opt/rabbitmq/sbin/rabbitmq-plugins enable rabbitmq_recent_history_exchange
elif [ "$(expr substr $(uname -s) 1 5)" == "Linux" ]; then
    sudo apt-get install rabbitmq
fi

# Install ksonnet
if [ "$(uname)" == "Darwin" ]; then
    brew install ksonnet/tap/ks
elif [ "$(expr substr $(uname -s) 1 5)" == "Linux" ]; then
    sudo apt-get install ksonnet
fi

# Install kubernetes
if [ "$(uname)" == "Darwin" ]; then
    brew install kubernetes-cli
elif [ "$(expr substr $(uname -s) 1 5)" == "Linux" ]; then
	sudo apt-get update && sudo apt-get install -y apt-transport-https
	curl -s https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key add -
	echo "deb https://apt.kubernetes.io/ kubernetes-xenial main" | sudo tee -a /etc/apt/sources.list.d/kubernetes.list
	sudo apt-get update
	sudo apt-get install -y kubectl
fi
