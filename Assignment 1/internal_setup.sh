#!/bin/bash

sudo apt-get update                                 # update packages
echo y | sudo apt-get install python-dev python-pip # install python pip
sudo pip install numpy flask                        # install dependencies
gunzip lookbusy.tar.gz                              # unpack lookbusy
tar xvf lookbusy.tar
cd lookbusy-1.4
./configure
sudo make install
cd ~
export FLASK_APP=internal_server.py
python -m flask run --host=0.0.0.0 --port=8080 &    # run server