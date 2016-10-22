#!/usr/bin/env python

import os
import sys
import time
from novaclient.v2 import client

IMAGE_NAME = 'ubuntu-14.04'
FLAVOR_NAME = 'm1.small'
NETWORK_NAME = 'internal network'
SECURITY_GROUP_NAME = 'default'
KEY_NAME = 'default'

def _get_nova_creds():
    d = {}
    d['version'] = '2'  # version 2 of the API
    d['region_name'] = os.environ['OS_REGION_NAME']
    d['auth_url'] = os.environ['OS_AUTH_URL']
    d['project_id'] = os.environ['OS_TENANT_NAME']
    d['tenant_id'] = os.environ['OS_TENANT_ID']
    d['username'] = os.environ['OS_USERNAME']
    d['api_key'] = os.environ['OS_PASSWORD']
    print 'Nova credentials loaded from the environment.'
    return d

def _create_connection(creds):
    try:
        nova = client.client.Client(**creds)
        print 'Nova connection created.'
    except:
        print 'Exception thrown: ', sys.exc_info()[0]
        raise
    return nova

def _generate_server_name(nova):
    names = set(server.name for server in nova.servers.list())
    index = 0
    name = 'rad_server_{0}'.format(index)
    while name in names:
        index += 1
        name = 'rad_server_{0}'.format(index)
    print 'New server name generated: {0}'.format(name)
    return name

def _create_server(nova):
    nameref = _generate_server_name(nova)
    imageref = nova.images.find(name=IMAGE_NAME)
    flavorref = nova.flavors.find(name=FLAVOR_NAME)
    netref = nova.networks.find(label=NETWORK_NAME)

    attrs = {
        'name' : nameref,
        'image' : imageref,
        'flavor' : flavorref,
        'security_groups' : [SECURITY_GROUP_NAME],
        'key_name' : KEY_NAME,
        'nics' : [{'net-id' : netref.id}]
    }

    try:
        server = nova.servers.create(**attrs)
    except:
        print 'Exception thrown: ', sys.exc_info()[0]
        raise

    print 'Starting server...'
    while(server.status != 'ACTIVE'):
        time.sleep(5)                              # sleep for 5 seconds
        server = nova.servers.find(name=nameref)   # refresh status

    print 'Server is now running'
    return server

def _get_unassigned_floating_ip(nova):
    for ip in nova.floating_ips.list():
        if not ip.instance_id:
            return ip
    return None

def _assign_floating_ip(nova, server):
    floating_ip = _get_unassigned_floating_ip(nova)
    if floating_ip:
        try:
            server.add_floating_ip(address=floating_ip)
            print 'Floating IP {0} assigned to server.'.format(floating_ip.ip)
            # refresh server after adding floating ip
            server = nova.servers.find(name=server.name)
        except:
            print 'Exception thrown: ', sys.exc_info()[0]
            server.delete()
            raise
        return server

# Interface

def spawn(has_floating_ip=False):
    creds = _get_nova_creds()
    nova = _create_connection(creds)
    server = _create_server(nova)
    if has_floating_ip:
        server = _assign_floating_ip(nova, server)
    return server

def get_ip(server, ip_type='fixed'):
    try:
        for addrs in server.addresses['internal network']:
            if addrs['OS-EXT-IPS:type'] == ip_type:
                return addrs['addr']
    except:
        print 'Exception thrown: ', sys.exc_info()[0]
        raise
    return None
