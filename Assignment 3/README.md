## Assignment 3 Project Page

Steps
1. Copy your ssh private key to this directory.<br>
2. **bootstrap.sh**: modify SSH_PEM to the name for your ssh private key.<br>
3. **playbook.yml**: add your username and password for the horizon cloud. Change the key path and name to you ssh private key name.<br>
4. run `vagrant up`<br>
5. ssh into the spawned vm using `ssh -i <private_key> -o StrictHostKeyChecking=no ubuntu@<floating_ip>`<br>
6. [Optional] Downloading the data seems to fail often, so I've included a small subset of the data just to demonstrate that the program works. You may opt to replace it by downloading the full data. To download the data, first set environment variables using `source <resource_file>`<br>
7. [Optional] Run `python obj_retrieve.py` to fetch the data.<br>
8. run `chmod 700 mapreduce.py`<br>
9. run `sudo docker run -v /home/ubuntu:/assign3 -it -d --name test python:2.7.9` to install the python 2.7.9 docker image<br>
10. run `sudo docker exec test python /assign3/mapreduce.py /assign3/energy-sorted100M.csv` to run the mapreduce program<br>
11. cleanup your spawned vm manually<br>