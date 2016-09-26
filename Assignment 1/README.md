The entry point for the program is run.sh.
The client program is named client.py.
The tier 2 server is named server.py.
The tier 2 VMs are setup using server.sh.
The tier 3 server is named internal_server.py.
The tier 3 VMs are setup using internal_server.py.
The Nova interface is used in manager.py.

To run the programs (which are not yet fully functional):
1) Run your .openrc.sh file to export your openstack credentials into the environment
2) Copy your private key to access the VMs (the source code references default.pem, so you may want to change either the name or the reference)
3) Run ./run.sh