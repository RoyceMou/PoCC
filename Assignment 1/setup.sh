#!/bin/bash

sudo apt-get update                                 # update packages
chmod 600 default.pem                               # modify user rights
echo y | sudo apt-get install python-dev python-pip # install python pip
sudo pip install python-novaclient flask            # install dependencies
echo Dependences installed
export FLASK_APP=server.py
python -m flask run --host=0.0.0.0 --port=8080 &    # run server