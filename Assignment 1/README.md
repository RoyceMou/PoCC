The entry point for the program is run.sh.<br>
The client program is named client.py.<br>
The tier 2 server is named server.py.<br>
The tier 2 VMs are setup using server.sh.<br>
The tier 3 server is named internal_server.py.<br>
The tier 3 VMs are setup using internal_server.py.<br>
The Nova interface is used in manager.py.<br>
The LookBusy zip is named lookbusy.tar.gz.<br>

To run the programs (which are not yet fully functional):<br>
1) Run your .openrc.sh file to export your openstack credentials into the environment<br>
2) Copy your private key to access the VMs.<br>
   The simplest way to make this work is to rename your private key to 'default.pem' and rename the constant 'KEY_NAME' in manager.py to the name of your private key.<br>
3) Run ./run.sh
