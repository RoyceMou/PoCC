#!/bin/python

import sys
import time
import signal
import httplib
import subprocess
from flask import Flask
from flask import request

app = Flask(__name__)

# internal_servers = []
internal_servers = []
policy = None
ratio = 1
count = 0   # represents the number of times that the second server has been chosen
PORT = '8080'

@app.route('/')
def welcome():
    return 'Welcome to the 2nd tier server for Assignment 1!'

@app.route('/extend')
def extend():
    print request.args
    if 't3_addr' in request.args:
        ip = request.args['t3_addr']
        print 'Received internal ip'
        internal_servers.append(ip)

        target = '{0}@{1}'.format('ubuntu', ip)

        files = ['internal_server.py', 'internal_setup.sh', 'lookbusy.tar.gz']
        copy_cmd = 'scp -o StrictHostKeyChecking=no -i default.pem {0} {1}:~'.format(' '.join(files), target)
        setup_cmd = 'ssh -n -f -i default.pem {0} "sh -c \'nohup bash internal_setup.sh > /dev/null 2>&1 &\'"'.format(target)

        time.sleep(20)                          # wait for ssh server to start
        subprocess.call(copy_cmd.split())       # copy files
        subprocess.call(setup_cmd, shell=True)  # setup vm
        time.sleep(120)                         # wait for web server to start
        return 'Added internal server: {0}'.format(ip)
    else:
        return 't3_addr unspecified.'


# selects the server to send the request to depending on the policy
def select_server():
    if policy is None:
        ip = internal_servers[0]
    else:
        if policy == 'RR':
            ip = internal_servers[1] if count < 1 else internal_servers[0]
            count = count + 1 if count < 1 else 0
        if policy == 'PD':
            ip = internal_servers[1] if count < ratio else internal_servers[0]
            count = count + 1 if count < ratio else 0
    return ip

# The following is to handle an incoming request for the dummy operation
# which is supposed to relay it to our 3rd tier VM according to the load
# balancing strategy
@app.route('/dummy_op')
def dummy_op():

    print 'Received request'
    print 'policy', policy
    print 'internal_servers', internal_servers

    ip = select_server()

    print 'Connecting to tier 3 server: {0}'.format(ip)
    conn = httplib.HTTPConnection(ip, PORT)
    conn.request('GET', '/dummy_op')
    resp = conn.getresponse().read()
    return 'Response from tier 3 server {0}: {1}'.format(ip, resp)

# The following is to handle an incoming request for autoscaling and the
# suggested policy
@app.route('/autoscale')
def autoscale():
    # @@@ NOTE @@@
    # here you should handle the autoscaling policy and take the steps
    # to start a new 3rd tier VM that will run the same code as the other VM.
    # You should also set the LB policy(round robin or proportional)

    # We expect the incoming request of the form
    # http://IPAddr/autoscale?lb=RR or
    # http://IPAddr/autoscale?lb=PD&ratio=1:5
    #
    # where RR = round robin(1:1 ratio implied),
    #       PD = proportional dispatch with ratio specified in the next param

    print 'Received request = {0}'.format(request)
    
    ret_msg = 'Welcome to Assignment 1 Server: autoscale! '
    # make sure that the load balancing strategy is mentioned
    if 'lb' in request.args:
        policy = 'RR' if request.args['lb'] == 'RR' else 'PD' if request.args['lb'] == 'PD' else None
        ret_msg += '{0} policy specified.'
    else:
        ret_msg += 'Request must provide at least the lb parameter. '

    if request.args['lb'] == 'PD':
        if 'ratio' in request.args: # expect the ration arg
            ratio = request.args['ratio'].split(':')
            ratio = int(ratio[1]) / int(ratio[0])
            ret_msg += 'Ratio = 1:{0}'.format(ratio)
        else:
            ret_msg += 'Ratio expected for proportional dispatch'
        
    return ret_msg


@app.route('/lookbusy')
def lookbusy():
    if len(internal_servers) < 1:
        return 'No internal servers found.'
    target = '{0}@{1}'.format('ubuntu', internal_servers[0])
    start_lookbusy = 'ssh -i default.pem {0} lookbusy -c 99 -r fixed -m 1gb -d 1gb'.format(target)
    subprocess.call(start_lookbusy, shell=True)  # setup vm
    return 'Lookbusy started on {0}'.format(internal_servers[0])


# def cleanup(signal, frame):
#     print 'Tier 2 server is being terminated. Terminating tier 3 servers.'
#     for server in internal_servers:
#         server.delete()
#     print 'Internal (tier 3) servers stopped.'
#     sys.exit(0)

# signal.signal(signal.SIGTERM, cleanup)

if __name__ == '__main__':
    print 'Client-facing (tier 2) server started.'
    app.run()  # make server public