#!/usr/bin/env python

from __future__ import print_function
from pyVim.connect import SmartConnect, SmartConnectNoSSL, Disconnect
from pyVmomi import vim
import atexit
import sys
import argparse
import re
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

def get_args():
    parser = argparse.ArgumentParser(
        description='Arguments for talking to vCenter')

    parser.add_argument('-s', '--host',
                        default='192.168.137.80',
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
                        default='jeeseen0307!@#$',
                        action='store',
                        help='Password to use')


    parser.add_argument('-c', '--skip_verification',
                        required=False,
                        action='store_true',
                        help='Skip SSL verification')

    parser.add_argument('-r', '--regex_esxi',
                        required=False,
                        default=None,
                        action='store',
                        help='Regex esxi name')

    args = parser.parse_args()
    return args


def GetVMHosts(content, regex_esxi=None):
    host_view = content.viewManager.CreateContainerView(content.rootFolder,
                                                        [vim.HostSystem],
                                                        True)
    obj = [host for host in host_view.view]
    match_obj = []
    if regex_esxi:
        for esxi in obj:
            if re.findall(r'%s.*' % regex_esxi, esxi.name):
                match_obj.append(esxi)
        match_obj_name = [match_esxi.name for match_esxi in match_obj]
        print("Matched ESXi hosts: %s" % match_obj_name)
        host_view.Destroy()
        return match_obj
    else:
        host_view.Destroy()
        return obj


def AddHostsPortgroup(hosts, vswitchName, portgroupName, vlanId):
    for host in hosts:
        AddHostPortgroup(host, vswitchName, portgroupName, vlanId)


def AddHostPortgroup(host, vswitchName, portgroupName, vlanId):
    portgroup_spec = vim.host.PortGroup.Specification()
    portgroup_spec.vswitchName = vswitchName
    portgroup_spec.name = portgroupName
    portgroup_spec.vlanId = int(vlanId)
    network_policy = vim.host.NetworkPolicy()
    network_policy.security = vim.host.NetworkPolicy.SecurityPolicy()
    network_policy.security.allowPromiscuous = True
    network_policy.security.macChanges = False
    network_policy.security.forgedTransmits = False
    portgroup_spec.policy = network_policy

    host.configManager.networkSystem.AddPortGroup(portgroup_spec)


def main():
    args = get_args()
    if args.skip_verification:
        serviceInstance = SmartConnectNoSSL(host=args.host,
                                            user=args.user,
                                            pwd=args.password,
                                            port=443)
    else:
        serviceInstance = SmartConnect(host=args.host,
                                       user=args.user,
                                       pwd=args.password,
                                       port=443)
    atexit.register(Disconnect, serviceInstance)
    content = serviceInstance.RetrieveContent()

    print (args.regex_esxi)

    hosts = GetVMHosts(content, args.regex_esxi)
    a = [
    ]##‘vlanid’,'ID','vswitch'
    for ceshi in a:
        AddHostsPortgroup(hosts, ceshi[2], ceshi[0], int(ceshi[1]))


# Main section
if __name__ == "__main__":
    sys.exit(main())
