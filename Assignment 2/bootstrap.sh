#!/bin/bash

# apt-get install software-properties-common
# apt-add-repository ppa:ansible/ansible
# apt-get update
# apt-get install -y ansible

# # CHANGE CONSTANTS HERE
# export SERVER_IP="129.59.107.80"
# export SSH_PEM="default.pem"

# # generate ansible hosts file
# echo -e "[server]\n" >> /etc/ansible/hosts 
# echo $SERVER_IP >> /etc/ansible/hosts 
# echo "Ansible hosts file generated"

# ### START CLIENT SETUP
# apt-get install -y python python-dev python-pip build-essential libssl-dev libffi-dev
# pip install shade
# # TODO might need to install ssl here
# ### END CLIENT SETUP
# echo "Client setup finished"

# # ansible config
# cp /etc/ansible/ansible.cfg ~/.ansible.cfg
# echo -e "[defaults]\nhost_key_checking = false " >> ~/.ansible.cfg
# echo "Ansible Configured"

# run server playbook

# export OS_AUTH_URL=https://keystone.isis.vanderbilt.edu:5000/v2.0

# # With the addition of Keystone we have standardized on the term **tenant**
# # as the entity that owns the resources.
# export OS_TENANT_ID=7b7cacfc1d3c4973a2666a26cf1a40ff
# export OS_TENANT_NAME="Cloud Class"

# # In addition to the owning entity (tenant), openstack stores the entity
# # performing the action as the **user**.
# export OS_USERNAME="mour"

# # With Keystone you pass the keystone password.
# echo "Please enter your OpenStack Password: "
# read -sr OS_PASSWORD_INPUT
# export OS_PASSWORD=$OS_PASSWORD_INPUT

# # If your configuration has multiple regions, we set that information here.
# # OS_REGION_NAME is optional and only valid in certain environments.
# export OS_REGION_NAME="regionOne"

ssh-agent bash
ssh-add $SSH_PEM
# chmod 700 /vagrant/playbook_server.yml
ansible-playbook /vagrant/playbook_server.yml
# ansible-playbook playbook_server.yml --sudo --connection=ssh

# run python client
# python client.py $SERVER_IP

# TODO: Is output from client.py stdout?
