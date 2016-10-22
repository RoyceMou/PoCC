#!/bin/bash

apt-get install software-properties-common
apt-add-repository ppa:ansible/ansible
apt-get update
apt-get install -y ansible

# CHANGE CONSTANTS HERE
export SERVER_IP="129.59.107.80"
export SSH_PEM="default.pem"

# generate ansible hosts file
echo -e "[server]\n" >> /etc/ansible/hosts 
echo $SERVER_IP >> /etc/ansible/hosts 

### START CLIENT SETUP
apt-get install -y python python-dev python-pip
sudo apt-get install build-essential libssl-dev libffi-dev python-dev
pip install shade
# TODO might need to install ssl here
### END CLIENT SETUP

# ansible config
cp /etc/ansible/ansible.cfg ~/.ansible.cfg
echo -e "[defaults]\nhost_key_checking = false " >> ~/.ansible.cfg

# run server playbook

ssh-agent bash
ssh-add $SSH_PEM
ansible-playbook playbook_server.yml
# ansible-playbook playbook_server.yml --sudo --connection=ssh

# run python client
# python client.py $SERVER_IP

# TODO: Is output from client.py stdout?
