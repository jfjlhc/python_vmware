

import atexit

from pyVmomi import vim, vmodl
from pyVim import connect
from pyVim.connect import Disconnect
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

inputs = {'vcenter_ip': '192.168.134.231',
          'vcenter_password': 'pass2017!@#$',
          'vcenter_user': 'jfj',
          'host_name': '192.168.134.99',
          'switch_name': 'vSwitch2',
          'port_group_name': 'Test1'
          }


def get_obj(content, vimtype, name):
    """
     Get the vsphere object associated with a given text name
    """
    obj = None
    container = content.viewManager.CreateContainerView(content.rootFolder, vimtype, True)
    for c in container.view:
        if c.name == name:
            obj = c
            break
    return obj




def create_port_group(host_network_system, pg_name, vss_name ,vlan_ID):
    port_group_spec = vim.host.PortGroup.Specification()
    port_group_spec.name = pg_name
    port_group_spec.vlanId = vlan_ID
    port_group_spec.vswitchName = vss_name

    security_policy = vim.host.NetworkPolicy.SecurityPolicy()
    security_policy.allowPromiscuous = True
    security_policy.forgedTransmits = True
    security_policy.macChanges = False

    port_group_spec.policy = vim.host.NetworkPolicy(security=security_policy)

    host_network_system.AddPortGroup(portgrp=port_group_spec)

    print ("Successfully created PortGroup ",  pg_name)


def main():

    try:
        si = None
        try:
            print ("Trying to connect to VCENTER SERVER . . .")
            si = connect.Connect(inputs['vcenter_ip'], 443, inputs['vcenter_user'], inputs['vcenter_password'], version="vim.version.version8")
        except (IOError, e):
            pass
            atexit.register(Disconnect, si)

        print ("Connected to VCENTER SERVER !")

        content = si.RetrieveContent()

        host = get_obj(content, [vim.HostSystem], inputs['host_name'])

        host_network_system = host.configManager.networkSystem

        a=[
            ['test1', 1106],
            ['test2', 0],
            ['test3', 1106],
        ]
        for ceshi in a:

                create_port_group(host_network_system, ceshi[0], inputs['switch_name'],int(ceshi[1]))


    except vmodl.MethodFault as e:
        print ("Caught vmodl fault: %s" % e.msg)
        return 1
    except Exception as  e:
        print ("Caught exception: %s" % str(e))
        return 1

# Start program
if __name__ == "__main__":
    main()