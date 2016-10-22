#!/bin/python

import sys
import time
import signal
import httplib
import subprocess
from flask import Flask
from flask import request

app = Flask(__name__)

@app.route('/')
def welcome():
    return 'Welcome to the server for Assignment 2!\n'

# The following is to handle an incoming request for the dummy operation
# which is supposed to relay it to our 3rd tier VM according to the load
# balancing strategy
@app.route('/dummy_op')
def dummy_op():
    print 'dummy_op'
    
    start_time = time.time()
    arr = np.random.random((1200,1200))
    arr_inv = linalg.inv(arr)
    end_time = time.time()
    
    return 'dummy_op completed in {0} seconds\n'.format(end_time - start_time)

# def cleanup(signal, frame):
#     print 'Tier 2 server is being terminated. Terminating tier 3 servers.'
#     for server in internal_servers:
#         server.delete()
#     print 'Internal (tier 3) servers stopped.'
#     sys.exit(0)

# signal.signal(signal.SIGTERM, cleanup)

if __name__ == '__main__':
    print 'Assignment 2 server started.'
    app.run()  # make server public