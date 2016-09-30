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
    
    files = ['default.pem', 'setup.sh', 'server.py', 'internal_setup.sh', 'internal_server.py']
    copy_cmd = 'scp -o StrictHostKeyChecking=no -i default.pem {0} {1}:~'.format(' '.join(files), target)
    # setup_cmd = 'ssh -n -f -i default.pem {0} "sh -c \'nohup ./setup.sh > /dev/null 2>&1 &\'"'.format(target)
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
    conn.request('GET', '/extend?t3_addr={0}'.format(ip_t3))
    resp = conn.getresponse().read()
    print resp

    # TODO: works until here. we need to configure the server to work for the dummy op
    x_axis = []
    y_axis = []
    num_times = 100
    print 'Sending request for the dummy op {0} times'.format(num_times)
    for i in range(1, num_times):
        start_time = time.time()
        conn.request('GET', '/dummy_op')
        resp = conn.getresponse().read()
        print resp
        end_time = time.time()
        time_elapsed = end_time - start_time
        print time_elapsed
        x_axis.append(i)
        y_axis.append(time_elapsed)
        

    # print 'Increasing load on the VM'
    # conn.request('GET', '/lookbusy')
    # resp = conn.getresponse().read()

    # print 'Sending request to autoscale with RR'
    # conn.request('GET', '/autoscale?lb=RR')

    # print 'Sending request to autoscale with PD'
    # conn.request('GET', '/autoscale?lb=PD&ratio=1:4')
    
    print 'Sending request for the dummy op {0} times'.format(num_times)
    for i in range(1, num_times):
        start_time = time.time()
        conn.request('GET', '/dummy_op')
        resp = conn.getresponse().read()
        print resp
        end_time = time.time()
        time_elapsed = end_time - start_time
        print time_elapsed
        x_axis.append(i)
        y_axis.append(time_elapsed)
        
    plt.plot(x_axis,y_axis)
    plt.ylabel("Response time")
    plt.title("Time to Respond to Requests")
    plt.show()
    plt.savefig("ResponseTime.png")
    

    # # sending a different kind of request. Here we send the autoscale
    # # request.
    # # @@@ Note @@@
    # # I have not shown any code to start the second VM on the 3rd tier.
    # # You should be including the IP addr of the 2nd VM on the 3rd tier
    # # in this autoscale request so the client-facing server now has the
    # # knowledge of the 2nd VM in the 3rd tier.
    
    # server.delete()
    
# invoke main
if __name__ == '__main__':
    sys.exit(main())
    
