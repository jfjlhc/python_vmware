#coding=utf-8
#!/usr/bin/python
import time
import sys
import ssl
import random
from pyVmomi import vim
from pyVim.connect import SmartConnect, Disconnect
import atexit

class Mac_address(object):

    def __init__(self,si,vmguest):
        self._si = si
        self.vmguest = vmguest
        self.get_obj()

    def get_obj(self):

        self._content = self._si.content
        self.object = self._content.viewManager.CreateContainerView(self._content.rootFolder,[vim.VirtualMachine],True)


        print(self.vmguest)
        for self._vm in self.object.view:
            try:
                if self._vm.name == self.vmguest:
                    self._obj = self._vm
                    break
            except Exception as e:
                print ("has a error", str(e))
        self.vm_name = self._obj.name
        self.object.Destroy()


    def _get_obj(self,vimtype, obj_name):

        self.object = self._content.viewManager.CreateContainerView(self._content.rootFolder,[vimtype],True)
        for self.type in self.object.view:
            try:
                if self.type.name == obj_name:
                    self.vlan_obj = type
                    break
            except Exception as e:
                print ("has a error", str(e))
        self.object.Destroy()

    def randomMAC(self):
        mac = [ 0x52, 0x56, 0x00,
                random.randint(0x00, 0x7f),
                random.randint(0x00, 0xff),
                random.randint(0x00, 0xff) ]
        return ':'.join(map(lambda x: "%02x" % x, mac))


def set_vc_si(host,user,port,password,context):
    try:
        si1 = SmartConnect(host=host, user=user,pwd=password,
                          port=port, sslContext=context)
        if not si1:
            print ("Can't connect to the host with given user and password")
            sys.exit()

        atexit.register(Disconnect, si1)


    except Exception as e:
        print ("catch the exception: ", str(e))
    return si1




def get_vc_si():
    host = "192.168.134.231"##vc can modify ip address
    user = "jfj"
    password = "pass2017!@#$"
    port = 443
    if host:
        context = ssl.create_default_context()
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE
    else:
        if hasattr(ssl, '_create_unverified_context'):
            context = ssl._create_unverified_context()


    si = set_vc_si(host, user, port, password, context)
    atexit.register(Disconnect, si)
    return si


def vm_runstatus(vm_obj):
    while True:
        system_ready = vm_obj.guest.guestOperationsReady
        system_state = vm_obj.guest.guestState
        system_uptime = vm_obj.summary.quickStats.uptimeSeconds
        if system_ready and system_state == 'running':
            break
        time.sleep(10)

def modify(old_vlanname,new_vlan_name):

    virtualmachine = "orcl-1"
    ip = "192.168.190.100"
    netmask = "255.255.255.0"
    gateway = "192.168.190.1"
    dns = ['114.114.114.114', '8.8.8.8']
    hostname = "centos"
    domain = "jfj.com"

    si = get_vc_si()

    jfj = Mac_address(si=si,vmguest=virtualmachine)
    newmac = jfj.randomMAC()
    print(newmac)
    nic_device = None
    for device in jfj._obj.config.hardware.device:
        if isinstance(device, vim.vm.device.VirtualEthernetCard) and device.deviceInfo.summary == old_vlanname:
            nic_device = device



    """修改mac地址,相当于手动编辑虚拟机，编辑设置-手动-修改MAC，系统的rules文件会自动增加一个mac配置信息"""
    try:
        print ("判断虚拟机的状态：")
        if jfj._obj.guest.guestState == "running":
            jfj._obj.PowerOff()
            time.sleep(3)

        virtual_nic_spec = vim.vm.device.VirtualDeviceSpec()
        virtual_nic_spec.operation = vim.vm.device.VirtualDeviceSpec.Operation.edit
        virtual_nic_spec.device = nic_device
        virtual_nic_spec.device.macAddress = newmac##最好和原来虚拟机存在的MAC不一致
        virtual_nic_spec.device.backing = nic_device.backing
        virtual_nic_spec.device.backing.deviceName = new_vlan_name

        dev_changes = []
        dev_changes.append(virtual_nic_spec)
        config_mac = vim.vm.ConfigSpec()
        config_mac.deviceChange = dev_changes
        print ("开始修改MAC地址")
        jfj._obj.ReconfigVM_Task(spec=config_mac)

        """修改IP地址"""
        print("修改mac地址完毕，开始修改IP地址")
        globalip = vim.vm.customization.GlobalIPSettings()
        adaptermap = vim.vm.customization.AdapterMapping()
        adaptermap.adapter = vim.vm.customization.IPSettings()
        adaptermap.adapter.dnsDomain = domain
        adaptermap.adapter.ip = vim.vm.customization.FixedIp(ipAddress=ip)
        adaptermap.adapter.subnetMask = netmask
        adaptermap.adapter.gateway = gateway
        globalip.dnsServerList = dns

        customspec = vim.vm.customization.Specification()
        identity = vim.vm.customization.LinuxPrep(domain=domain,hostName=vim.vm.customization.FixedName(name=hostname))
        customspec.identity = identity
        customspec.nicSettingMap = [adaptermap]
        customspec.globalIPSettings = globalip
        jfj._obj.CustomizeVM_Task(spec=customspec)


    except Exception as e:
        print(e)
        # if hasattr(e,'msg'):
        #     msg = e.msg.decode('utf-8')
        #     print (msg)
        # else:
        #     print ("the error is",str(e))

if __name__ == "__main__":
    modify(old_vlanname="vlan126",
           new_vlan_name="vlan126")