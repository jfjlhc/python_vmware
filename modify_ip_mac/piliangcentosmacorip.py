# !/usr/bin/env python3
# coding=utf-8
from pyVim.connect import SmartConnect, Disconnect
from pyVmomi import vim, vmodl
from getpass import getpass
import numpy as np
import atexit
import argparse
import sys
import ssl
"""批量修改CENTOS地址"""
ssl._create_default_https_context = ssl._create_unverified_context

resourcepool = 'kktest'    #需要检测的资源池
luser='root'                #linux机器的账号
lpwd ='123456'              #linux机器的密码

linuxdan = [
            ['192.168.133.69', '255.255.255.192', '192.168.133.65', '114.114.114.114'],
            ['192.168.133.75', '255.255.255.192', '192.168.133.65', '114.114.114.114'],
            ['192.168.133.78', '255.255.255.192', '192.168.133.65', '114.114.114.114']
        ]

linuxshuang=[
            ['192.168.133.70', '255.255.255.192', '192.168.133.65', '114.114.114.114',
            '192.168.60.70', '255.255.255.0', '192.168.60.1', '114.114.114.114'],
            ['192.168.133.71', '255.255.255.192', '192.168.133.65', '114.114.114.114',
             '192.168.60.71', '255.255.255.0', '192.168.60.1', '114.114.114.114'],
            ['192.168.133.72', '255.255.255.192', '192.168.133.65', '114.114.114.114',
             '192.168.60.72', '255.255.255.0', '192.168.60.1', '114.114.114.114'],
            ['192.168.133.73', '255.255.255.192', '192.168.133.65', '114.114.114.114',
             '192.168.60.73', '255.255.255.0', '192.168.60.1', '114.114.114.114'],
            ['192.168.133.74', '255.255.255.192', '192.168.133.65', '114.114.114.114',
             '192.168.60.74', '255.255.255.0', '192.168.60.1', '114.114.114.114'],
            ]



def options():
    parser = argparse.ArgumentParser(prog='exec-guestos-cmd',
                                     add_help=True)
    parser.add_argument('--host', '-vc',
                        type=str, default='192.168.134.99')
    parser.add_argument('--username', '-u',
                        type=str, default='root')
    parser.add_argument('--password', '-p',
                        type=str, default='JcatPass0197')

    args = parser.parse_args()
    return args


def login(args):
    context = None
    if hasattr(ssl, '_create_unverified_context'):
        context = ssl._create_unverified_context()

    si = SmartConnect(host=args.host,
                      user=args.username,
                      pwd=args.password,
                      sslContext=context)

    atexit.register(Disconnect, si)

    content = si.content

    return content


def get_mob_info(content, mob, target=''):
    # print (content,mob,target)
    # print
    r = content.viewManager.CreateContainerView(content.rootFolder,
                                                [mob],
                                                True)

    if (target):
        for i in r.view:
            if (i.name == target):
                r = i

    return r


def check_vmware_tools_status(vm_mob):
    vmware_tools_status = vm_mob.guest.toolsStatus
    if (not (vmware_tools_status == 'toolsOk')):
        sys.stderr.write("%s: VMware tools\n" % vm_mob.name)
        #sys.exit(1)
        print('vmtools not running')
    else:
        print('vmtools ok')

def linuxVmInformation1(vm):
    try:
        summary = vm.summary
        name= summary.vm.resourcePool.name
        xitong = summary.config.guestFullName
        network =vm.summary.config.numEthernetCards
        vmtoolstatus = vm.summary.guest.toolsStatus
        if vmtoolstatus =='toolsOk':
            if xitong == 'CentOS 4/5/6/7 (64-bit)':
                if name == resourcepool:
                    if network == 1:
                        b = [summary.config.name]
                        return b
    except:
        pass

def linuxVmInformation2(vm):
    try:
        summary = vm.summary
        name= summary.vm.resourcePool.name
        xitong = summary.config.guestFullName
        network =vm.summary.config.numEthernetCards
        vmtoolstatus = vm.summary.guest.toolsStatus
        if vmtoolstatus =='toolsOk':
            if xitong == 'CentOS 4/5/6/7 (64-bit)':
                if name == resourcepool:
                    if network == 2:
                        b = [summary.config.name]
                        return b
    except:
        pass

def linux1(args):
    # ServiceContent.
    content = login(args)
    lit = []
    for datacenter in content.rootFolder.childEntity:
        if hasattr(datacenter.vmFolder, 'childEntity'):
            vmFolder = datacenter.vmFolder
            vmList = vmFolder.childEntity
            for xxvxx in vmList:
                d = linuxVmInformation1(xxvxx)
                if d != None:
                    x = d
                    for ceshi in x:
                        lit.append(ceshi)

    return lit

def linux2(args):
    # ServiceContent.
    content = login(args)
    lit = []
    for datacenter in content.rootFolder.childEntity:
        if hasattr(datacenter.vmFolder, 'childEntity'):
            vmFolder = datacenter.vmFolder
            vmList = vmFolder.childEntity
            for xxvxx in vmList:
                d = linuxVmInformation2(xxvxx)#返回数组
                if d != None:
                    x = d
                    for ceshi in x:
                        lit.append(ceshi)

    return lit

def main3():
    args = options()#自定义参数
    content = login(args)#连接vc返回si.content
    user = luser#虚拟机用户
    passwd = lpwd#虚拟机密码
    test = linux1(args)#返回虚拟机名字的列表
    print("虚拟机的名字列表：\n", test)
    a2=linuxdan#单网卡ip地址网关DNS列表
    x = np.array(test)#虚拟机名字列表
    print("虚拟机的名字列表使用numpy多维数组：\n",x)
    # print
    d = x.reshape(len(test), 1)#改变列出的形状，列表长度作为行的数目，1列
    print ("虚拟机名字改变形状之后：\n",d)
    # print
    c = np.array(a2)#IP、网关、DNS列表
    print ("用户预先输入的IP和网关等信息：\n",c)
    # print
    changdu = len(test)
    a = c[0:changdu, ]#取资源池中符合单网卡的虚拟机个数的IP网关DNS信息列表，打印出来即可了解
    print ("取出虚拟机个数的IP信息：\n",a)

    k = np.array(a)
    print ("取出虚拟机个数的IP信息使用numpy多维数组：\n",k)

    ceshi = np.hstack((d, k))
    print ("end:\n",ceshi)
    # print
    for i in ceshi:
        #print ("i的值是：\n",i[1])
        vm_mob = get_mob_info(content, vim.VirtualMachine, i[0])#返回虚拟机实例对象
        check_vmware_tools_status(vm_mob)#检查虚拟机的vmtools安装情况
        guest_auth = vim.vm.guest.NamePasswordAuthentication()#验证虚拟机用户密码
        guest_auth.username = user#虚拟机的用户名
        guest_auth.password = passwd#虚拟机的系统密码

        guest_program_spec = vim.vm.guest.ProcessManager.ProgramSpec()#获取网卡名字eth0
        guest_program_spec.arguments = "a=`ip addr |grep -v lo | grep mtu |sed -n '1p'|awk -F ':' '{print$2}' |sed 's/^[[:space:]]*//g'` >> /1.sh "
        guest_program_spec.programPath = '/bin/echo'

        guest_program_specD = vim.vm.guest.ProcessManager.ProgramSpec()#获取网卡的MAC地址
        guest_program_specD.arguments = "b=`ip addr |grep ether |awk '{print$2}'` >> /1.sh "
        guest_program_specD.programPath = '/bin/echo'

        guest_program_specA = vim.vm.guest.ProcessManager.ProgramSpec()
        guest_program_specA.arguments = "  rm -rf /etc/sysconfig/network-scripts/ifcfg-e\*>> /1.sh "
        guest_program_specA.programPath = '/bin/echo'

        guest_program_spec1 = vim.vm.guest.ProcessManager.ProgramSpec()
        guest_program_spec1.arguments = "touch /etc/sysconfig/network-scripts/ifcfg-\$a >> /1.sh "
        guest_program_spec1.programPath = '/bin/echo'

        guest_program_spec2 = vim.vm.guest.ProcessManager.ProgramSpec()
        guest_program_spec2.arguments = "'echo \"DEVICE=$a\" >> /etc/sysconfig/network-scripts/ifcfg-$a ' >> /1.sh "
        guest_program_spec2.programPath = '/bin/echo'

        guest_program_spec3 = vim.vm.guest.ProcessManager.ProgramSpec()
        guest_program_spec3.arguments = "'echo \"ONBOOT=yes\" >> /etc/sysconfig/network-scripts/ifcfg-$a ' >> /1.sh "
        guest_program_spec3.programPath = '/bin/echo'

        guest_program_spec4 = vim.vm.guest.ProcessManager.ProgramSpec()
        guest_program_spec4.arguments = "'echo \"TYPE=Ethernet\" >> /etc/sysconfig/network-scripts/ifcfg-$a ' >> /1.sh "
        guest_program_spec4.programPath = '/bin/echo'

        guest_program_spec5 = vim.vm.guest.ProcessManager.ProgramSpec()
        guest_program_spec5.arguments = "'echo \"BOOTPROTO=static\" >> /etc/sysconfig/network-scripts/ifcfg-$a ' >> /1.sh "
        guest_program_spec5.programPath = '/bin/echo'

        guest_program_spec6 = vim.vm.guest.ProcessManager.ProgramSpec()
        guest_program_spec6.arguments = "'echo \"HWADDR=$b\" >> /etc/sysconfig/network-scripts/ifcfg-$a ' >> /1.sh "
        guest_program_spec6.programPath = '/bin/echo'

        guest_program_spec7 = vim.vm.guest.ProcessManager.ProgramSpec()
        guest_program_spec7.arguments = "'echo \"IPADDR=\""+i[1]+">> /etc/sysconfig/network-scripts/ifcfg-$a ' >> /1.sh "
        guest_program_spec7.programPath = '/bin/echo'

        guest_program_spec8 = vim.vm.guest.ProcessManager.ProgramSpec()
        guest_program_spec8.arguments = "'echo \"GATEWAY=\""+i[3]+" >> /etc/sysconfig/network-scripts/ifcfg-$a ' >> /1.sh "
        guest_program_spec8.programPath = '/bin/echo'

        guest_program_spec9 = vim.vm.guest.ProcessManager.ProgramSpec()
        guest_program_spec9.arguments = "'echo \"NETMASK=\""+i[2]+" >> /etc/sysconfig/network-scripts/ifcfg-$a ' >> /1.sh "
        guest_program_spec9.programPath = '/bin/echo'

        guest_program_specB = vim.vm.guest.ProcessManager.ProgramSpec()
        guest_program_specB.arguments = "'echo \"DNS1=\""+i[4]+">> /etc/sysconfig/network-scripts/ifcfg-$a ' >> /1.sh "
        guest_program_specB.programPath = '/bin/echo'

        guest_program_specC = vim.vm.guest.ProcessManager.ProgramSpec()
        guest_program_specC.arguments = "service network restart >> /1.sh "
        guest_program_specC.programPath = '/bin/echo'

        guest_program_specdel = vim.vm.guest.ProcessManager.ProgramSpec()
        guest_program_specdel.arguments = "rm -rf /1.sh >> /1.sh "
        guest_program_specdel.programPath = '/bin/echo'

        guest_program_specE = vim.vm.guest.ProcessManager.ProgramSpec()
        guest_program_specE.arguments = " /1.sh"
        guest_program_specE.programPath = '/bin/bash'

        r = content.guestOperationsManager.processManager.StartProgramInGuest(
            vm=vm_mob,
            auth=guest_auth,
            spec=guest_program_spec
        )
        g = content.guestOperationsManager.processManager.StartProgramInGuest(
            vm=vm_mob,
            auth=guest_auth,
            spec=guest_program_specD
        )

        y = content.guestOperationsManager.processManager.StartProgramInGuest(
            vm=vm_mob,
            auth=guest_auth,
            spec=guest_program_specA
        )

        b = content.guestOperationsManager.processManager.StartProgramInGuest(
            vm=vm_mob,
            auth=guest_auth,
            spec=guest_program_spec1
        )

        c = content.guestOperationsManager.processManager.StartProgramInGuest(
            vm=vm_mob,
            auth=guest_auth,
            spec=guest_program_spec2
        )
        d = content.guestOperationsManager.processManager.StartProgramInGuest(
            vm=vm_mob,
            auth=guest_auth,
            spec=guest_program_spec3
        )
        e = content.guestOperationsManager.processManager.StartProgramInGuest(
            vm=vm_mob,
            auth=guest_auth,
            spec=guest_program_spec4
        )

        m = content.guestOperationsManager.processManager.StartProgramInGuest(
            vm=vm_mob,
            auth=guest_auth,
            spec=guest_program_spec5
        )

        q = content.guestOperationsManager.processManager.StartProgramInGuest(
            vm=vm_mob,
            auth=guest_auth,
            spec=guest_program_spec6
        )

        t = content.guestOperationsManager.processManager.StartProgramInGuest(
            vm=vm_mob,
            auth=guest_auth,
            spec=guest_program_spec7
        )

        z = content.guestOperationsManager.processManager.StartProgramInGuest(
            vm=vm_mob,
            auth=guest_auth,
            spec=guest_program_spec8
        )

        x = content.guestOperationsManager.processManager.StartProgramInGuest(
            vm=vm_mob,
            auth=guest_auth,
            spec=guest_program_spec9
        )

        v = content.guestOperationsManager.processManager.StartProgramInGuest(
            vm=vm_mob,
            auth=guest_auth,
            spec=guest_program_specB
        )

        n = content.guestOperationsManager.processManager.StartProgramInGuest(
            vm=vm_mob,
            auth=guest_auth,
            spec=guest_program_specC
        )

        de = content.guestOperationsManager.processManager.StartProgramInGuest(
            vm=vm_mob,
            auth=guest_auth,
            spec=guest_program_specdel
        )

        p = content.guestOperationsManager.processManager.StartProgramInGuest(
            vm=vm_mob,
            auth=guest_auth,
            spec=guest_program_specE
        )

        print('finish')


def main4():
    args = options()#自定义参数
    content = login(args)#连接vc返回si.content
    user = luser#虚拟机用户
    passwd = lpwd#虚拟机密码
    test = linux2(args)#返回双网卡的虚拟机名字的列表
    a3 =linuxshuang#双网卡ip地址网关DNS列表
    x = np.array(test)
    print(x)
    d = x.reshape(len(test), 1)
    c = np.array(a3)
    changdu = len(test)
    a = c[0:changdu, ]
    k = np.array(a)
    ceshi = np.hstack((d, k))
    for i in ceshi:
        vm_mob = get_mob_info(content, vim.VirtualMachine, i[0])
        check_vmware_tools_status(vm_mob)
        guest_auth = vim.vm.guest.NamePasswordAuthentication()
        guest_auth.username = user
        guest_auth.password = passwd

        guest_program_spec = vim.vm.guest.ProcessManager.ProgramSpec()
        guest_program_spec.arguments = "a=`ip addr |grep -v lo | grep mtu |sed -n '1p'|awk -F ':' '{print$2}' |sed 's/^[[:space:]]*//g'` >> /1.sh "
        guest_program_spec.programPath = '/bin/echo'

        guest_program_specD = vim.vm.guest.ProcessManager.ProgramSpec()
        guest_program_specD.arguments = "b=`ip addr |grep ether |sed -n '1p' |awk '{print$2}'` >> /1.sh "
        guest_program_specD.programPath = '/bin/echo'

        guest_program_specA = vim.vm.guest.ProcessManager.ProgramSpec()
        guest_program_specA.arguments = "  rm -rf /etc/sysconfig/network-scripts/ifcfg-e\*>> /1.sh "
        guest_program_specA.programPath = '/bin/echo'

        guest_program_spec1 = vim.vm.guest.ProcessManager.ProgramSpec()
        guest_program_spec1.arguments = "touch /etc/sysconfig/network-scripts/ifcfg-\$a >> /1.sh "
        guest_program_spec1.programPath = '/bin/echo'

        guest_program_spec2 = vim.vm.guest.ProcessManager.ProgramSpec()
        guest_program_spec2.arguments = "'echo \"DEVICE=$a\" >> /etc/sysconfig/network-scripts/ifcfg-$a ' >> /1.sh "
        guest_program_spec2.programPath = '/bin/echo'

        guest_program_spec3 = vim.vm.guest.ProcessManager.ProgramSpec()
        guest_program_spec3.arguments = "'echo \"ONBOOT=yes\" >> /etc/sysconfig/network-scripts/ifcfg-$a ' >> /1.sh "
        guest_program_spec3.programPath = '/bin/echo'

        guest_program_spec4 = vim.vm.guest.ProcessManager.ProgramSpec()
        guest_program_spec4.arguments = "'echo \"TYPE=Ethernet\" >> /etc/sysconfig/network-scripts/ifcfg-$a ' >> /1.sh "
        guest_program_spec4.programPath = '/bin/echo'

        guest_program_spec5 = vim.vm.guest.ProcessManager.ProgramSpec()
        guest_program_spec5.arguments = "'echo \"BOOTPROTO=static\" >> /etc/sysconfig/network-scripts/ifcfg-$a ' >> /1.sh "
        guest_program_spec5.programPath = '/bin/echo'

        guest_program_spec6 = vim.vm.guest.ProcessManager.ProgramSpec()
        guest_program_spec6.arguments = "'echo \"HWADDR=$b\" >> /etc/sysconfig/network-scripts/ifcfg-$a ' >> /1.sh "
        guest_program_spec6.programPath = '/bin/echo'

        guest_program_spec7 = vim.vm.guest.ProcessManager.ProgramSpec()
        guest_program_spec7.arguments = "'echo \"IPADDR=\""+i[1]+">> /etc/sysconfig/network-scripts/ifcfg-$a ' >> /1.sh "
        guest_program_spec7.programPath = '/bin/echo'

        guest_program_spec8 = vim.vm.guest.ProcessManager.ProgramSpec()
        guest_program_spec8.arguments = "'echo \"GATEWAY=\""+i[3]+" >> /etc/sysconfig/network-scripts/ifcfg-$a ' >> /1.sh "
        guest_program_spec8.programPath = '/bin/echo'

        guest_program_spec9 = vim.vm.guest.ProcessManager.ProgramSpec()
        guest_program_spec9.arguments = "'echo \"NETMASK=\""+i[2]+" >> /etc/sysconfig/network-scripts/ifcfg-$a ' >> /1.sh "
        guest_program_spec9.programPath = '/bin/echo'

        guest_program_specB = vim.vm.guest.ProcessManager.ProgramSpec()
        guest_program_specB.arguments = "'echo \"DNS1=\""+i[4]+">> /etc/sysconfig/network-scripts/ifcfg-$a ' >> /1.sh "
        guest_program_specB.programPath = '/bin/echo'

        guest_program_specC = vim.vm.guest.ProcessManager.ProgramSpec()
        guest_program_specC.arguments = "service network restart >> /1.sh "
        guest_program_specC.programPath = '/bin/echo'

        guest_program_specdel = vim.vm.guest.ProcessManager.ProgramSpec()
        guest_program_specdel.arguments = "rm -rf /1.sh >> /1.sh "
        guest_program_specdel.programPath = '/bin/echo'

        guest_program_specE = vim.vm.guest.ProcessManager.ProgramSpec()
        guest_program_specE.arguments = " /1.sh"
        guest_program_specE.programPath = '/bin/bash'

        guest_program_specAA = vim.vm.guest.ProcessManager.ProgramSpec()
        guest_program_specAA.arguments = "c=`ip addr |grep -v lo | grep mtu |sed -n '2p'|awk -F ':' '{print$2}' |sed 's/^[[:space:]]*//g'` >> /2.sh  "
        guest_program_specAA.programPath = '/bin/echo'

        guest_program_specA0 = vim.vm.guest.ProcessManager.ProgramSpec()
        guest_program_specA0.arguments = "d=`ip addr |grep ether |sed -n '2p' |awk '{print$2}'` >> /2.sh "
        guest_program_specA0.programPath = '/bin/echo'

        guest_program_specA1 = vim.vm.guest.ProcessManager.ProgramSpec()
        guest_program_specA1.arguments = "touch /etc/sysconfig/network-scripts/ifcfg-\$c >> /2.sh "
        guest_program_specA1.programPath = '/bin/echo'

        guest_program_specA2 = vim.vm.guest.ProcessManager.ProgramSpec()
        guest_program_specA2.arguments = "'echo \"DEVICE=$c\" >> /etc/sysconfig/network-scripts/ifcfg-$c ' >> /2.sh "
        guest_program_specA2.programPath = '/bin/echo'

        guest_program_specA3 = vim.vm.guest.ProcessManager.ProgramSpec()
        guest_program_specA3.arguments = "'echo \"HWADDR=$d\" >> /etc/sysconfig/network-scripts/ifcfg-$c ' >> /2.sh "
        guest_program_specA3.programPath = '/bin/echo'

        guest_program_specA4 = vim.vm.guest.ProcessManager.ProgramSpec()
        guest_program_specA4.arguments = "'echo \"TYPE=Ethernet\" >> /etc/sysconfig/network-scripts/ifcfg-$c ' >> /2.sh "
        guest_program_specA4.programPath = '/bin/echo'

        guest_program_specA5 = vim.vm.guest.ProcessManager.ProgramSpec()
        guest_program_specA5.arguments = "'echo \"BOOTPROTO=static\" >> /etc/sysconfig/network-scripts/ifcfg-$c ' >> /2.sh "
        guest_program_specA5.programPath = '/bin/echo'

        guest_program_specA6 = vim.vm.guest.ProcessManager.ProgramSpec()
        guest_program_specA6.arguments = "'echo \"ONBOOT=yes\" >> /etc/sysconfig/network-scripts/ifcfg-$c ' >> /2.sh "
        guest_program_specA6.programPath = '/bin/echo'

        guest_program_specA7 = vim.vm.guest.ProcessManager.ProgramSpec()
        guest_program_specA7.arguments = "'echo \"IPADDR=\""+i[5]+">> /etc/sysconfig/network-scripts/ifcfg-$c ' >> /2.sh "
        guest_program_specA7.programPath = '/bin/echo'


        guest_program_specA8 = vim.vm.guest.ProcessManager.ProgramSpec()
        guest_program_specA8.arguments = "'echo \"NETMASK=\""+i[6]+" >> /etc/sysconfig/network-scripts/ifcfg-$c ' >> /2.sh "
        guest_program_specA8.programPath = '/bin/echo'

        guest_program_specA9 = vim.vm.guest.ProcessManager.ProgramSpec()
        guest_program_specA9.arguments = "'echo \"GATEWAY=\""+i[7]+" >> /etc/sysconfig/network-scripts/ifcfg-$c ' >> /2.sh "
        guest_program_specA9.programPath = '/bin/echo'

        guest_program_specAB = vim.vm.guest.ProcessManager.ProgramSpec()
        guest_program_specAB.arguments = "'echo \"DNS1=\""+i[8]+" >> /etc/sysconfig/network-scripts/ifcfg-$c ' >> /2.sh "
        guest_program_specAB.programPath = '/bin/echo'

        guest_program_specAC = vim.vm.guest.ProcessManager.ProgramSpec()
        guest_program_specAC.arguments = "service network restart >> /2.sh "
        guest_program_specAC.programPath = '/bin/echo'

        guest_program_specdel1 = vim.vm.guest.ProcessManager.ProgramSpec()
        guest_program_specdel1.arguments = "rm -rf /2.sh >> /2.sh "
        guest_program_specdel1.programPath = '/bin/echo'

        guest_program_specAE = vim.vm.guest.ProcessManager.ProgramSpec()
        guest_program_specAE.arguments = " /2.sh"
        guest_program_specAE.programPath = '/bin/bash'

        r = content.guestOperationsManager.processManager.StartProgramInGuest(
            vm=vm_mob,
            auth=guest_auth,
            spec=guest_program_spec
        )
        g = content.guestOperationsManager.processManager.StartProgramInGuest(
            vm=vm_mob,
            auth=guest_auth,
            spec=guest_program_specD
        )

        y = content.guestOperationsManager.processManager.StartProgramInGuest(
            vm=vm_mob,
            auth=guest_auth,
            spec=guest_program_specA
        )

        b = content.guestOperationsManager.processManager.StartProgramInGuest(
            vm=vm_mob,
            auth=guest_auth,
            spec=guest_program_spec1
        )

        c = content.guestOperationsManager.processManager.StartProgramInGuest(
            vm=vm_mob,
            auth=guest_auth,
            spec=guest_program_spec2
        )
        d = content.guestOperationsManager.processManager.StartProgramInGuest(
            vm=vm_mob,
            auth=guest_auth,
            spec=guest_program_spec3
        )
        e = content.guestOperationsManager.processManager.StartProgramInGuest(
            vm=vm_mob,
            auth=guest_auth,
            spec=guest_program_spec4
        )

        m = content.guestOperationsManager.processManager.StartProgramInGuest(
            vm=vm_mob,
            auth=guest_auth,
            spec=guest_program_spec5
        )

        q = content.guestOperationsManager.processManager.StartProgramInGuest(
            vm=vm_mob,
            auth=guest_auth,
            spec=guest_program_spec6
        )

        t = content.guestOperationsManager.processManager.StartProgramInGuest(
            vm=vm_mob,
            auth=guest_auth,
            spec=guest_program_spec7
        )

        z = content.guestOperationsManager.processManager.StartProgramInGuest(
            vm=vm_mob,
            auth=guest_auth,
            spec=guest_program_spec8
        )

        x = content.guestOperationsManager.processManager.StartProgramInGuest(
            vm=vm_mob,
            auth=guest_auth,
            spec=guest_program_spec9
        )

        v = content.guestOperationsManager.processManager.StartProgramInGuest(
            vm=vm_mob,
            auth=guest_auth,
            spec=guest_program_specB
        )

        n = content.guestOperationsManager.processManager.StartProgramInGuest(
            vm=vm_mob,
            auth=guest_auth,
            spec=guest_program_specC
        )

        de = content.guestOperationsManager.processManager.StartProgramInGuest(
            vm=vm_mob,
            auth=guest_auth,
            spec=guest_program_specdel
        )

        p = content.guestOperationsManager.processManager.StartProgramInGuest(
            vm=vm_mob,
            auth=guest_auth,
            spec=guest_program_specE
        )


        r1 = content.guestOperationsManager.processManager.StartProgramInGuest(
            vm=vm_mob,
            auth=guest_auth,
            spec=guest_program_specAA
        )
        g1 = content.guestOperationsManager.processManager.StartProgramInGuest(
            vm=vm_mob,
            auth=guest_auth,
            spec=guest_program_specA0
        )

        b1 = content.guestOperationsManager.processManager.StartProgramInGuest(
            vm=vm_mob,
            auth=guest_auth,
            spec=guest_program_specA1
        )

        c1 = content.guestOperationsManager.processManager.StartProgramInGuest(
            vm=vm_mob,
            auth=guest_auth,
            spec=guest_program_specA2
        )
        d1 = content.guestOperationsManager.processManager.StartProgramInGuest(
            vm=vm_mob,
            auth=guest_auth,
            spec=guest_program_specA3
        )
        e1 = content.guestOperationsManager.processManager.StartProgramInGuest(
            vm=vm_mob,
            auth=guest_auth,
            spec=guest_program_specA4
        )

        m1 = content.guestOperationsManager.processManager.StartProgramInGuest(
            vm=vm_mob,
            auth=guest_auth,
            spec=guest_program_specA5
        )

        q1 = content.guestOperationsManager.processManager.StartProgramInGuest(
            vm=vm_mob,
            auth=guest_auth,
            spec=guest_program_specA6
        )

        t1 = content.guestOperationsManager.processManager.StartProgramInGuest(
            vm=vm_mob,
            auth=guest_auth,
            spec=guest_program_specA7
        )

        z1 = content.guestOperationsManager.processManager.StartProgramInGuest(
            vm=vm_mob,
            auth=guest_auth,
            spec=guest_program_specA8
        )

        x1 = content.guestOperationsManager.processManager.StartProgramInGuest(
            vm=vm_mob,
            auth=guest_auth,
            spec=guest_program_specA9
        )

        v1 = content.guestOperationsManager.processManager.StartProgramInGuest(
            vm=vm_mob,
            auth=guest_auth,
            spec=guest_program_specAB
        )

        n1 = content.guestOperationsManager.processManager.StartProgramInGuest(
            vm=vm_mob,
            auth=guest_auth,
            spec=guest_program_specAC
        )

        de1 = content.guestOperationsManager.processManager.StartProgramInGuest(
            vm=vm_mob,
            auth=guest_auth,
            spec=guest_program_specdel1
        )

        p1 = content.guestOperationsManager.processManager.StartProgramInGuest(
            vm=vm_mob,
            auth=guest_auth,
            spec=guest_program_specAE
        )

        print('finish')
if __name__ == "__main__":

    main3()     #更改单网卡linux/centos
    main4()     #更改双网卡linux/centos

    print('all ok')








