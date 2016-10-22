#!/bin/bash

apt-get install software-properties-common
apt-add-repository ppa:ansible/ansible
apt-get update
apt-get install -y ansible

# CHANGE CONSTANTS HERE
export SERVER_IP="129.59.107.80"
export SSH_PEM="/vagrant/peck_ashley.pem"

# generate ansible hosts file
echo -e "[server]\n" >> /etc/ansible/hosts 
echo $SERVER_IP >> /etc/ansible/hosts 
echo "Ansible hosts file generated"

### START CLIENT SETUP
apt-get install -y python python-dev python-pip build-essential libssl-dev libffi-dev
pip install shade
# TODO might need to install ssl here
### END CLIENT SETUP
echo "Client setup finished"

# ansible config
cp /etc/ansible/ansible.cfg ~/.ansible.cfg
echo -e "[defaults]\nhost_key_checking = false" >> ~/.ansible.cfg
# echo -e "[defaults]\nhost_key_checking = false\nprivate_key_file = /vagrant/" >> ~/.ansible.cfg
# echo -n $SSH_PEM >> ~/.ansible.cfg
echo "Ansible Configured"

# run server playbook

ssh-agent bash
chmod 700 $SSH_PEM
ssh-add $SSH_PEM
ansible-playbook /vagrant/playbook_server.yml
# ansible-playbook playbook_server.yml --sudo --connection=ssh

ansible server –m copy –a "src=/vagrant/server.py dest=~/server.py" –u ubuntu
ansible server -a "sudo apt-get install -y python-dev python-pip" -u ubuntu
ansible server -a "pip install flask numpy" -u ubuntu



# run python client
# python client.py $SERVER_IP

# TODO: Is output from client.py stdout?
