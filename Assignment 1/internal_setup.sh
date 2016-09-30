#!/usr/bin/bash

sudo apt-get update									# update packages
echo y | sudo apt-get install python-dev python-pip	# install python pip
sudo pip install numpy flask						# install dependencies
export FLASK_APP=internal_server.py
python -m flask run --host=0.0.0.0 --port=8080 &	# run server