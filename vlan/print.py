#!/usr/bin/env python
"""
Written by nickcooper-zhangtonghao
Github: https://github.com/nickcooper-zhangtonghao
Email: nickcooper-zhangtonghao@opencloud.tech
Note: Example code For testing purposes only
This code has been released under the terms of the Apache-2.0 license
http://opensource.org/licenses/Apache-2.0
"""

from __future__ import print_function
from pyVim.connect import SmartConnect, Disconnect
from pyVmomi import vim
import atexit
import sys
import argparse
import ssl
import re
ssl._create_default_https_context = ssl._create_unverified_context

def get_args():
    parser = argparse.ArgumentParser(
        description='Arguments for talking to vCenter')

    parser.add_argument('-s', '--host',
                        default='192.168.137.104',
                        action='store',
                        help='vSpehre service to connect to')

    parser.add_argument('-o', '--port',
                        type=int,
                        default=443,
                        action='store',
                        help='Port to connect on')

    parser.add_argument('-u', '--user',
                        default='root',
                        action='store',
                        help='User name to use')

    parser.add_argument('-p', '--password',
                        default='Jeeseen.com.run1225!@#$',
                        action='store',
                        help='Password to use')

    args = parser.parse_args()
    return args


def GetVMHosts(content):
    host_view = content.viewManager.CreateContainerView(content.rootFolder,
                                                        [vim.HostSystem],
                                                        True)
    obj = [host for host in host_view.view]
    host_view.Destroy()
    # print (obj)#['vim.HostSystem:ha-host']
    # print
    return obj


def GetHostsPortgroups(hosts):

    hostPgDict = {}
    for host in hosts:
        pgs = host.config.network.portgroup
        # print (pgs)
        # print
        hostPgDict[host] = pgs
        # print (hostPgDict)
        # print
    return hostPgDict

def main():
    args = get_args()
    serviceInstance = SmartConnect(host=args.host,
                                   user=args.user,
                                   pwd=args.password,
                                   port=443)
    atexit.register(Disconnect, serviceInstance)
    content = serviceInstance.RetrieveContent()

    hosts = GetVMHosts(content)#主机名字数组

    hostPgDict = GetHostsPortgroups(hosts)
    for portgroups in hostPgDict.items():
        for b in portgroups:
            print(b)

# Main section
if __name__ == "__main__":
    sys.exit(main())
