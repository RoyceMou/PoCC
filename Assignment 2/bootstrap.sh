#!/bin/bash

apt-get install software-properties-common
apt-add-repository ppa:ansible/ansible
apt-get update
apt-get install -y ansible

export SERVER_IP="129.59.107.80"

# generate ansible hosts file
echo -e "[server]\n" >> /etc/ansible/hosts 
echo $SERVER_IP >> /etc/ansible/hosts 

### START CLIENT SETUP
apt-get install -y python python-dev python-pip
pip install shade
# TODO might need to install ssl here
### END CLIENT SETUP

# ansible config
cp /etc/ansible/ansible.cfg ~/.ansible.cfg
echo -e "[defaults]\nhost_key_checking = false " >> ~/.ansible.cfg

# run server playbook
ansible-playbook playbook_server.yml
# ansible-playbook playbook_server.yml --sudo --remote-user=ubuntu --connection=ssh

# run python client
python client.py $SERVER_IP

# TODO: Is output from client.py stdout?
