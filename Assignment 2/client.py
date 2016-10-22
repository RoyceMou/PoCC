#!/bin/python

import sys
import httplib
import time

PORT = '8080'

def request(connection, path, display_response=False, display_time=False):
    start_time = time.time()
    connection.request('GET', path)    
    response = connection.getresponse().read()
    end_time = time.time()
    if display_response:
        print 'Response from server:', response
    time_elapsed = end_time - start_time
    if display_time:
        print 'Connection request took {0} seconds'.format(time_elapsed)
    return time_elapsed

def main(ip):
    # @@@ NOTE @@@
    # In your code, you should first start the main client-facing server on the
    # horizon cloud. See my sample code nova_server_create.py on how to do
    # this. You will need to do a bit more to that file so that it can
    # be imported here and you can use the functions. 
    #
    # Once the main server is active, also proceed to start the first VM on the
    # 3rd tier. Inform the client-facing server the IP address of the
    # 3rd tier VM so that the client-facing server can relay your requests
    # to that VM thereafter.

    print 'Connecting to server: {0}'.format(ip)
    conn = httplib.HTTPConnection(ip, PORT)

    num_times = 10
    print 'Sending request for the dummy op {0} times'.format(num_times)
    for i in range(1, num_times):
        time_elapsed = request(conn, '/dummy_op', display_response=True, display_time=True)
        print 'Time elapsed:', time_elapsed

    # # sending a different kind of request. Here we send the autoscale
    # # request.
    # # @@@ Note @@@
    # # I have not shown any code to start the second VM on the 3rd tier.
    # # You should be including the IP addr of the 2nd VM on the 3rd tier
    # # in this autoscale request so the client-facing server now has the
    # # knowledge of the 2nd VM in the 3rd tier.
    
# invoke main
if __name__ == '__main__':
    try:
        ip = sys.argv[1]
        sys.exit(main(ip))
    except IndexError:
        print 'usage: python client.py <ip_addr>'
    # e.g.: python client.py 129.59.107.80