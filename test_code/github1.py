#!/usr/bin/env python
"""
NOTE:
This gist has been moved to EZmomi:
   https://github.com/snobear/ezmomi

Give it a star or fork.  Contributions are more than welcome.  I'm hoping it will become an easy cli tool for
common VMware tasks.
(Notes from the original gist start here)
Example usage:
  ./clone.py --hostname test01 --template CentOS65 --ips 172.9.9.11 172.12.120.22 --cpus 2 --mem 4
Pip requirements:
-----------------
ecdsa==0.10
netaddr==0.7.10
pycrypto==2.6.1
pyvmomi==5.5.0
wsgiref==0.1.2
"""

from pyVim.connect import SmartConnect, Disconnect
from pyVmomi import vim, vmodl
import atexit
import os
import sys
from pprint import pprint, pformat
import time
from netaddr import IPNetwork, IPAddress
import argparse
import getpass
from settings import *
from copy import deepcopy

"""
 Send an email
"""


def send_email(deploy_settings, ip_settings, output):
    # Import smtplib for the actual sending function
    import smtplib
    from email.mime.text import MIMEText

    me = os.getenv("SUDO_USER")  # who ran sudo
    if me is None:
        me = os.getenv("USER")  # will always be root when this scripts is run as sudo

    email_body = "%s" % output
    msg = MIMEText(email_body)
    msg['Subject'] = "%s - VM deploy complete" % deploy_settings["new_vm_name"]
    msg['From'] = deploy_settings["mailfrom"]
    msg['To'] = me

    s = smtplib.SMTP('localhost')
    s.sendmail(deploy_settings["mailfrom"], [me], msg.as_string())
    s.quit()


"""
 Waits and provides updates on a vSphere task
"""


def WaitTask(task, actionName='job', hideResult=False):
    # print 'Waiting for %s to complete.' % actionName

    while task.info.state == vim.TaskInfo.State.running:
        time.sleep(2)

    if task.info.state == vim.TaskInfo.State.success:
        if task.info.result is not None and not hideResult:
            out = '%s completed successfully, result: %s' % (actionName, task.info.result)
        else:
            out = '%s completed successfully.' % actionName
    else:
        out = '%s did not complete successfully: %s' % (actionName, task.info.error)
        print
        out
        raise task.info.error  # should be a Fault... check XXX

    # may not always be applicable, but can't hurt.
    return task.info.result


"""
 Get the vsphere object associated with a given text name
"""


def get_obj(content, vimtype, name):
    obj = None
    container = content.viewManager.CreateContainerView(content.rootFolder, vimtype, True)
    for c in container.view:
        if c.name == name:
            obj = c
            break
    return obj


"""
 Connect to vCenter server and deploy a VM from template
"""


def clone(deploy_settings, ip_settings):
    fqdn = "%s.%s" % (deploy_settings["new_vm_name"], ip_settings[0]["domain"])

    # connect to vCenter server
    try:
        si = SmartConnect(host=deploy_settings["vserver"], user=deploy_settings["username"],
                          pwd=deploy_settings["password"], port=int(deploy_settings["port"]))
    except IOError as e:
        sys.exit("Unable to connect to vsphere server. Error message: %s" % e)

    # add a clean up routine
    atexit.register(Disconnect, si)

    content = si.RetrieveContent()

    # get the vSphere objects associated with the human-friendly labels we supply
    datacenter = get_obj(content, [vim.Datacenter], ip_settings[0]["datacenter_name"])
    # get the folder where VMs are kept for this datacenter
    destfolder = datacenter.vmFolder

    cluster = get_obj(content, [vim.ClusterComputeResource], ip_settings[0]["cluster_name"])
    resource_pool = cluster.resourcePool  # use same root resource pool that my desired cluster uses
    datastore = get_obj(content, [vim.Datastore], ip_settings[0]["datastore_name"])
    template_vm = get_obj(content, [vim.VirtualMachine], deploy_settings["template_name"])

    # Relocation spec
    relospec = vim.vm.RelocateSpec()
    relospec.datastore = datastore
    relospec.pool = resource_pool

    '''
     Networking config for VM and guest OS
    '''
    devices = []
    adaptermaps = []

    # create a Network device for each static IP
    for key, ip in enumerate(ip_settings):
        # VM device
        nic = vim.vm.device.VirtualDeviceSpec()
        nic.operation = vim.vm.device.VirtualDeviceSpec.Operation.add  # or edit if a device exists
        nic.device = vim.vm.device.VirtualVmxnet3()
        nic.device.wakeOnLanEnabled = True
        nic.device.addressType = 'assigned'
        nic.device.key = 4000  # 4000 seems to be the value to use for a vmxnet3 device
        nic.device.deviceInfo = vim.Description()
        nic.device.deviceInfo.label = "Network Adapter %s" % (key + 1)
        nic.device.deviceInfo.summary = ip_settings[key]["network_name"]
        nic.device.backing = vim.vm.device.VirtualEthernetCard.NetworkBackingInfo()
        nic.device.backing.network = get_obj(content, [vim.Network], ip_settings[key]["network_name"])
        nic.device.backing.deviceName = ip_settings[key]["network_name"]
        nic.device.backing.useAutoDetect = False
        nic.device.connectable = vim.vm.device.VirtualDevice.ConnectInfo()
        nic.device.connectable.startConnected = True
        nic.device.connectable.allowGuestControl = True
        devices.append(nic)

        # guest NIC settings, i.e. "adapter map"
        guest_map = vim.vm.customization.AdapterMapping()
        guest_map.adapter = vim.vm.customization.IPSettings()
        guest_map.adapter.ip = vim.vm.customization.FixedIp()
        guest_map.adapter.ip.ipAddress = str(ip_settings[key]["ip"])
        guest_map.adapter.subnetMask = str(ip_settings[key]["subnet_mask"])

        # these may not be set for certain IPs, e.g. storage IPs
        try:
            guest_map.adapter.gateway = ip_settings[key]["gateway"]
        except:
            pass

        try:
            guest_map.adapter.dnsDomain = ip_settings[key]["domain"]
        except:
            pass

        adaptermaps.append(guest_map)

    # VM config spec
    vmconf = vim.vm.ConfigSpec()
    vmconf.numCPUs = deploy_settings['cpus']
    vmconf.memoryMB = deploy_settings['mem']
    vmconf.cpuHotAddEnabled = True
    vmconf.memoryHotAddEnabled = True
    vmconf.deviceChange = devices

    # DNS settings
    globalip = vim.vm.customization.GlobalIPSettings()
    globalip.dnsServerList = deploy_settings['dns_servers']
    globalip.dnsSuffixList = ip_settings[0]['domain']

    # Hostname settings
    ident = vim.vm.customization.LinuxPrep()
    ident.domain = ip_settings[0]['domain']
    ident.hostName = vim.vm.customization.FixedName()
    ident.hostName.name = deploy_settings["new_vm_name"]

    customspec = vim.vm.customization.Specification()
    customspec.nicSettingMap = adaptermaps
    customspec.globalIPSettings = globalip
    customspec.identity = ident

    # Clone spec
    clonespec = vim.vm.CloneSpec()
    clonespec.location = relospec
    clonespec.config = vmconf
    clonespec.customization = customspec
    clonespec.powerOn = True
    clonespec.template = False

    # fire the clone task
    task = template_vm.Clone(folder=destfolder, name=deploy_settings["new_vm_name"].title(), spec=clonespec)
    result = WaitTask(task, 'VM clone task')

    # send notification
    send_email(deploy_settings, ip_settings, output)


def main(**kwargs):
    deploy_settings["new_vm_name"] = kwargs['hostname'].lower()
    deploy_settings['cpus'] = kwargs['cpus']
    deploy_settings['mem'] = kwargs['mem'] * 1024

    # initialize a list to hold our network settings
    ip_settings = list()

    '''
    Get settings for each IP given
    '''
    for key, ip_string in enumerate(kwargs['ips']):

        # convert ip from string to the "IPAddress" type
        ip = IPAddress(ip_string)

        # determine network this IP is in
        for network_address in net:
            if ip in network_address:
                net[network_address]["ip"] = ip
                ip_settings.append(net[network_address])

        # throw an error if we couldn't find a network for this ip
        if not any(d['ip'] == ip for d in ip_settings):
            sys.exit("ERROR: I don't know what network %s is in.  Please add settings for this network." % ip_string)

    # our default domain
    if 'domain' not in ip_settings[0]:
        ip_settings[0]['domain'] = 'example.com'

    # what VM template to use
    deploy_settings['template_name'] = kwargs['template']

    # clone template to a new VM with our specified settings
    clone(deploy_settings, ip_settings)


"""
 Main program
"""
if __name__ == "__main__":
    if getpass.getuser() != 'root':
        sys.exit("You must be root to run this.  Quitting.")

    # Define command line arguments
    parser = argparse.ArgumentParser(description='Deploy a new VM in vSphere')
    parser.add_argument('--template', type=str, help='VMware template to clone', default='CentOS65')
    parser.add_argument('--hostname', type=str, required=True, help='New host name', )
    parser.add_argument('--ips', type=str, help='Static IPs of new host, separated by a space', nargs='+',
                        required=True)
    parser.add_argument('--cpus', type=int, help='Number of CPUs', default=1)
    parser.add_argument('--mem', type=int, help='Memory in GB', default=3)

    # Parse arguments and hand off to main()
    args = parser.parse_args()
    main(**vars(args))