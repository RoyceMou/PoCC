#!/bin/python

import sys
import httplib
import manager
import time
import subprocess
import random
import matplotlib.pyplot as plt
plt.figure()

PORT = '8080'

def spawn_t2():
    server = manager.spawn(has_floating_ip=True)
    ip = manager.get_ip(server, ip_type='floating')
    target = '{0}@{1}'.format('ubuntu', ip)
    
    files = ['default.pem', 'setup.sh', 'server.py', 'internal_setup.sh', 'internal_server.py', 'lookbusy.tar.gz']
    copy_cmd = 'scp -o StrictHostKeyChecking=no -i default.pem {0} {1}:~'.format(' '.join(files), target)
    # setup_cmd = 'ssh -n -f -i default.pem {0} 'sh -c \'nohup ./setup.sh > /dev/null 2>&1 &\'''.format(target)
    setup_cmd = 'ssh -n -f -i default.pem {0} "sh -c \'nohup bash setup.sh > /dev/null 2>&1 &\'"'.format(target)
    # setup_cmd = 'ssh -i default.pem {0} ~/setup.sh'.format(target)

    time.sleep(20)                          # wait for ssh server to start
    subprocess.call(copy_cmd.split())       # copy files
    subprocess.call(setup_cmd, shell=True)  # setup vm
    time.sleep(120)                         # wait for web server to start
    return server, ip

def spawn_t3():
    server = manager.spawn()
    ip = manager.get_ip(server)

    return server, ip

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

# main: In this sample code, we send a few requests:
# first a simple http message to the web server's main page and
# then the dummy_op request multiple times, an autoscale request with
# round robin policy, and finally an autoscale request with the proportional
# dispatch policy along with the ratio in which subsequent requests are
# going to be handled 
def main():
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

    # clear known hosts to prevent time out
    # subprocess.call('echo > ~/.ssh/known_hosts'.split())

    print 'Creating tier 2 server'
    server_t2, ip_t2 = spawn_t2()

    print 'Creating tier 3 server'
    server_t3, ip_t3 = spawn_t3()

    print 'Connecting to tier 2 server: {0}'.format(ip_t2)
    conn = httplib.HTTPConnection(ip_t2, PORT)

    print 'Extending internal servers'
    request(conn, '/extend?t3_addr={0}'.format(ip_t3))

    # TODO: works until here. we need to configure the server to work for the dummy op
    x_axis = []
    y_axis = []
    num_times = 12
    average = 0
    xcounter = 1
    print 'Sending request for the dummy op {0} times'.format(num_times)
    for i in range(1, num_times):
        time_elapsed = request(conn, '/dummy_op', display_time=True)
        print 'Time elapsed:', time_elapsed
        average += time_elapsed
        x_axis.append(xcounter)
        xcounter += 1
        y_axis.append(time_elapsed)
    average /= num_times
    print 'Average response times: {0}'.format(average)

    print 'Increasing load on the VM'
    request(conn, '/lookbusy', display_response=True)
    
    print 'Testing new response speed'
    time_elapsed = 0
    while time_elapsed <=  average * 1.2:
        time_elapsed = request(conn, '/dummy_op', display_time=True)
        print 'Time elapsed:', time_elapsed
        x_axis.append(xcounter)
        xcounter += 1
        y_axis.append(time_elapsed)
    print 'New response speed over 20% of previous average'

    print 'Creating new tier 3 server'
    server_t3_1, ip_t3_1 = spawn_t3()

    print 'Extending internal servers'
    request(conn, '/extend?t3_addr={0}'.format(ip_t3_1))

    # print 'Sending request to autoscale with round robin policy'
    # request(conn, '/autoscale?lb=RR', display_response=True)

    print 'Sending request to autoscale with proportional dispatch'
    request(conn, '/autoscale?lb=PD&ratio=1:4', display_response=True)

    print 'Sending request for the dummy op {0} times'.format(num_times)
    for i in range(1, num_times):
        time_elapsed = request(conn, '/dummy_op', display_time=True)
        print 'Time elapsed:', time_elapsed
        x_axis.append(xcounter)
        xcounter += 1
        y_axis.append(time_elapsed)
        
    plt.plot(x_axis,y_axis)
    plt.ylabel('Response time')
    plt.title('Time to Respond to Requests')    
    plt.savefig('ResponseTime.png')
    plt.show()
    

    # # sending a different kind of request. Here we send the autoscale
    # # request.
    # # @@@ Note @@@
    # # I have not shown any code to start the second VM on the 3rd tier.
    # # You should be including the IP addr of the 2nd VM on the 3rd tier
    # # in this autoscale request so the client-facing server now has the
    # # knowledge of the 2nd VM in the 3rd tier.
    
    server_t2.delete()
    server_t3.delete()
    server_t3_1.delete()
    
# invoke main
if __name__ == '__main__':
    sys.exit(main())
    
