#!/bin/python

import sys
import time
import signal
import numpy as np
import manager
from numpy import linalg
from flask import Flask
from flask import request

app = Flask(__name__)

@app.route('/')
def welcome():
    return 'Welcome to a 3rd tier server for Assignment 1!'

@app.route('/dummy_op')
def dummy_op():
    # you should be relaying the request to the 3rd tier according to
    # the LB strategy. Moreover, not only that, but you need to time the
    # request and reply the original client with the measured time
    #
    # If you expect to relay a param, that param must be received via
    # the http request. See autoscale method to see how we receive a param
    print 'dummy_op'
    
    # @@@@ NOTE @@@
    # this kind of logic which I have shown below should in fact be
    # executed on the 3rd tier server
    #
    # What am I doing below ?
    # We create an array of 1200x1200 and take its inverse. I am observing
    # around 5 secs to get this work done. For 2000x2000, I got around 24 secs.
    # I tried 5000x5000 but it seemed like it was never ending :-) so I gave up
    # I think a 5 sec resp time is good enough. With the machine getting loaded
    # the resp time should shoot up for our client to maybe double what we see.
    arr = np.random.random((1200,1200))
    arr_inv = linalg.inv(arr)
    
        # @@@ NOTE @@@
    # Here I am returning a message and the time it took.
    # On receipt of this time, the client should decide if the deviation
    # from historic resp time is greater than some percent, say 20%, in
    # which case, the client should invoke autoscale with the
    # appropriate strategy
    
    return 'Welcome to Assignment 1 Server: dummy_op! took %s time units' %(end_time - start_time)

if __name__ == '__main__':
    app.run()