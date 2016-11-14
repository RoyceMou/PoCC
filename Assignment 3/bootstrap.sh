#!/bin/bash

# CHANGE CONSTANTS HERE
SERVER_IP="129.59.107.80"
SSH_PEM="default.pem"

apt-get install software-properties-common
apt-add-repository ppa:ansible/ansible
apt-get update
apt-get install -y ansible

# generate ansible hosts file
echo -e "[server]\n" >> /etc/ansible/hosts 
echo $SERVER_IP >> /etc/ansible/hosts 
echo "Ansible hosts file generated"

# ansible config
# FOR SOME REASON, TILDE EXPANSION DOESN'T WORK
cp /etc/ansible/ansible.cfg /home/ubuntu/ansible.cfg
echo -e "[defaults]\nhost_key_checking = false" >> /home/ubuntu/ansible.cfg
# echo -e "[defaults]\nhost_key_checking = false\nprivate_key_file = /vagrant/" >> ~/ansible.cfg
# echo -n $SSH_PEM >> ~/ansible.cfg
echo "Ansible Configured"

# run server playbook
# chmod does not work on files in the /vagrant directory
cp /vagrant/$SSH_PEM /home/ubuntu/$SSH_PEM
chmod 600 /home/ubuntu/$SSH_PEM
ls -l /home/ubuntu/$SSH_PEM
# not sure if the two lines below are necessary or not
ssh-agent bash
ssh-add /home/ubuntu/$SSH_PEM
ansible-playbook /vagrant/playbook.yml --sudo --private-key /home/ubuntu/$SSH_PEM

# # run python client
python /vagrant/client.py $SERVER_IP

# cleanup
ansible-playbook /vagrant/cleanup.yml --sudo --private-key /home/ubuntu/$SSH_PEM