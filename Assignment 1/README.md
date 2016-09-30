The entry point for the program is run.sh.<br>
The client program is named client.py.<br>
The tier 2 server is named server.py.<br>
The tier 2 VMs are setup using server.sh.<br>
The tier 3 server is named internal_server.py.<br>
The tier 3 VMs are setup using internal_server.py.<br>
The Nova interface is used in manager.py.<br>
The LookBusy zip is named lookbusy.tar.gz.<br>

To run the programs (which are not yet fully functional):<br>
1) Run sudo pip install matplotlib
2) Run sudo apt-get install python-tk
3) Run your .openrc.sh file to export your openstack credentials into the environment<br>
4) Copy your private key to access the VMs (the source code references default.pem, so you may want to change either the name or the reference)<br>
5) Run ./run.sh
