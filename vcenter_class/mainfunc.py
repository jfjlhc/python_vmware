#coding=utf-8
import sys
from vcenter_class.kkx.vcrandom import rand_num
import random
import sys,time
from pyVmomi import vim,vmodl
names = locals()
"""my func"""



def WaitForTasks(tasks, si):
    """
    Given the service instance si and tasks, it returns after all the
    tasks are complete
    """
    pc = si.content.propertyCollector

    taskList = [str(task) for task in tasks]

    # Create filter
    objSpecs = [vmodl.query.PropertyCollector.ObjectSpec(obj=task) for task in tasks]
    propSpec = [vmodl.query.PropertyCollector.PropertySpec(type=vim.Task, pathSet=[], all=True)]
    filterSpec = vmodl.query.PropertyCollector.FilterSpec(objectSet=objSpecs, propSet=propSpec)
    filter = pc.CreateFilter(filterSpec, True)

    try:
        version, state = None, None

        # Loop looking for updates till the state moves to a completed state.
        while len(taskList):
            update = pc.WaitForUpdates(version)
            for filterSet in update.filterSet:
                for objSet in filterSet.objectSet:
                    task = objSet.obj
                    for change in objSet.changeSet:
                        if change.name == 'info':
                            state = change.val.state
                        elif change.name == 'info.state':
                            state = change.val
                        else:
                            continue

                        if not str(task) in taskList:
                            continue

                        if state == vim.TaskInfo.State.success:
                            # Remove task from taskList
                            taskList.remove(str(task))
                        elif state == vim.TaskInfo.State.error:
                            raise task.info.error
            # Move to next version
            version = update.version
    finally:
        if filter:
            filter.Destroy()
    return None

def get_host(content):
    obj = None
    objView = content.viewManager.CreateContainerView(content.rootFolder,
                                                      [vim.ComputeResource],
                                                      True)
    obj = objView.view
    objView.Destroy()
    return obj

def get_host_pool(content,all_obj_list,host_name):
    obj = None
    for host in all_obj_list:
        if host.name == host_name:
            objView = content.viewManager.CreateContainerView(host,
                                                               [vim.ResourcePool],
                                                               True)
            obj = objView.view
            objView.Destroy()
            break
    return obj

def get_host_pool_vm(content,pool_obj_list,pool_name):
    obj = None
    for pool in pool_obj_list:
        if pool.name == pool_name:
            objView = content.viewManager.CreateContainerView(pool,
                                                              [vim.VirtualMachine],

                                                              True)
            obj = objView.view
            objView.Destroy()
            break
    return obj

def get_obj(content, vimtype, name):
    obj = None
    try:
        if content == None:
            return Exception
        container = content.viewManager.CreateContainerView(content.rootFolder, [vimtype], True)
        for c in container.view:
            if c.name == name:
                obj = c
                break
        return obj
    except Exception as e:
        errormsg = sys._getframe().f_code.co_filename, sys._getframe().f_code.co_name, sys._getframe().f_lineno
        print (errormsg,"没有得到obj")


def vm_runstatus(vm_obj):
    while True:
        system_ready = vm_obj.guest.guestOperationsReady
        system_state = vm_obj.guest.guestState
        system_uptime = vm_obj.summary.quickStats.uptimeSeconds
        if system_ready and system_state == 'running':
            break
        time.sleep(5)
        break


def randomMAC():
    mac = [0x52, 0x56, 0x00,
           random.randint(0x00, 0x7f),
           random.randint(0x00, 0xff),
           random.randint(0x00, 0xff)]
    return ':'.join(map(lambda x: "%02x" % x, mac))

def delete_adapter(vm,si):
    """删除网卡"""

    try:

        print("判断虚拟机的状态：")

        while True:
            if vm.summary.guest.toolsStatus == "toolsOk":
                print("你好虚拟机正在运行，现在进行关闭虚拟机")
                tasks = [vm.PowerOff()]
                WaitForTasks(tasks, si)
                time.sleep(1)
                break
            elif vm.summary.guest.toolsStatus == "toolsNotRunning":
                print("你好虚拟机正处于关闭状态:")
                break
            else:
                tasks = [vm.PowerOff()]
                WaitForTasks(tasks, si)
                break

        obj = []
        nic = []
        for nic_dev in vm.config.hardware.device:
            if isinstance(nic_dev, vim.vm.device.VirtualVmxnet3):
                obj.append(nic_dev)
            elif isinstance(nic_dev,vim.vm.device.VirtualE1000):
                nic.append(nic_dev)

        if len(obj) > 0:
            print("vmxnet3 eq:",len(obj))
            for device in obj:

                add_nic_spec = vim.vm.device.VirtualDeviceSpec()
                add_nic_spec.operation = vim.vm.device.VirtualDeviceSpec.Operation.remove
                add_nic_spec.device = device
                add_netspec = []
                add_netspec.append(add_nic_spec)
                add_network = vim.vm.ConfigSpec()
                add_network.deviceChange = add_netspec

                print("开始删除网卡")
                tasks = [vm.ReconfigVM_Task(spec=add_network)]
                WaitForTasks(tasks, si)

        if len(nic) > 0:
            print("E1000:",len(nic))
            for device in nic:
                add_nic_spec = vim.vm.device.VirtualDeviceSpec()
                add_nic_spec.operation = vim.vm.device.VirtualDeviceSpec.Operation.remove
                add_nic_spec.device = device
                add_netspec = []
                add_netspec.append(add_nic_spec)
                add_network = vim.vm.ConfigSpec()
                add_network.deviceChange = add_netspec

                print("开始删除网卡")
                tasks = [vm.ReconfigVM_Task(spec=add_network)]
                WaitForTasks(tasks, si)
        print("删除网卡完毕！程序继续往下执行")

    except Exception as e:
        errormsg = sys._getframe().f_code.co_filename, sys._getframe().f_code.co_name, sys._getframe().f_lineno
        if hasattr(e, 'msg'):
            msg = e.msg
            print (errormsg,msg)
            sys.exit(1)
        else:
            print ("the error is",errormsg, str(e))
            sys.exit(1)

def add_adapter(vm_obj,vlan_name,net_obj,si):
    """增加网卡，没有设置IP"""

    try:
        numm = str(rand_num(2))
        print("判断虚拟机的状态：")

        while True:
            if vm_obj.summary.guest.toolsStatus == "toolsOk":
                print("你好虚拟机正在运行，现在进行关闭虚拟机")
                tasks = [vm_obj.PowerOff()]
                WaitForTasks(tasks, si)
                time.sleep(1)
                break
            elif vm_obj.summary.guest.toolsStatus == "toolsNotRunning":
                print("你好虚拟机正处于关闭状态:")
                break
            else:
                tasks = [vm_obj.PowerOff()]
                WaitForTasks(tasks, si)
                break

        add_nic_spec = vim.vm.device.VirtualDeviceSpec()
        add_nic_spec.operation = vim.vm.device.VirtualDeviceSpec.Operation.add
        add_nic_spec.device = vim.vm.device.VirtualVmxnet3()
        add_nic_spec.device.wakeOnLanEnabled = True
        add_nic_spec.device.backing = vim.vm.device.VirtualEthernetCard.NetworkBackingInfo()
        add_nic_spec.device.backing.deviceName = vlan_name
        add_nic_spec.device.backing.network = net_obj  # jfj._get_obj(vim.Network, vlan_name)
        add_nic_spec.device.connectable = vim.vm.device.VirtualDevice.ConnectInfo()
        add_nic_spec.device.connectable.connected = True
        add_nic_spec.device.connectable.allowGuestControl = True
        add_nic_spec.device.connectable.startConnected =True

        add_netspec = []
        add_netspec.append(add_nic_spec)
        add_network = vim.vm.ConfigSpec()
        add_network.deviceChange = add_netspec

        print ("开始增加网卡")
        tasks = [vm_obj.ReconfigVM_Task(spec=add_network)]
        WaitForTasks(tasks,si)


    except Exception as e:
        errormsg = sys._getframe().f_code.co_filename, sys._getframe().f_code.co_name, sys._getframe().f_lineno
        if hasattr(e, 'msg'):
            msg = e.msg
            print (errormsg,msg)
            sys.exit(1)
        else:
            print ("the error is",errormsg, str(e))
            sys.exit(1)


def add_linux_adapter(vm_obj,vlan_name,net_obj,si,domain,new_ip,netmask,dns,gateway,num):
    """增加网卡"""

    try:
        numm = str(rand_num(2))
        print("判断虚拟机的状态：")

        while True:
            if vm_obj.summary.guest.toolsStatus == "toolsOk":
                print("你好虚拟机正在运行，现在进行关闭虚拟机")
                tasks = [vm_obj.PowerOff()]
                WaitForTasks(tasks, si)
                time.sleep(1)
                break
            elif vm_obj.summary.guest.toolsStatus == "toolsNotRunning":
                print("你好虚拟机正处于关闭状态:")
                break

        add_nic_spec = vim.vm.device.VirtualDeviceSpec()
        add_nic_spec.operation = vim.vm.device.VirtualDeviceSpec.Operation.add
        add_nic_spec.device = vim.vm.device.VirtualVmxnet3()
        add_nic_spec.device.wakeOnLanEnabled = True
        add_nic_spec.device.backing = vim.vm.device.VirtualEthernetCard.NetworkBackingInfo()
        add_nic_spec.device.backing.deviceName = vlan_name
        add_nic_spec.device.backing.network = net_obj  # jfj._get_obj(vim.Network, vlan_name)
        add_nic_spec.device.connectable = vim.vm.device.VirtualDevice.ConnectInfo()
        add_nic_spec.device.connectable.connected = True
        add_nic_spec.device.connectable.allowGuestControl = True
        add_nic_spec.device.connectable.startConnected =True

        add_netspec = []
        add_netspec.append(add_nic_spec)
        add_network = vim.vm.ConfigSpec()
        add_network.deviceChange = add_netspec

        print ("开始增加网卡")
        tasks = [vm_obj.ReconfigVM_Task(spec=add_network)]
        WaitForTasks(tasks,si)

        print("判断虚拟机的状态：")

        while True:
            if vm_obj.summary.guest.toolsStatus == "toolsOk":
                print("你好虚拟机正在运行，现在进行关闭虚拟机")
                tasks = [vm_obj.PowerOff()]
                WaitForTasks(tasks, si)
                time.sleep(1)
                break
            elif vm_obj.summary.guest.toolsStatus == "toolsNotRunning":
                print("你好虚拟机正处于关闭状态:")
                break

        print("虚拟机已经关闭客户机，{}开始修改IP".format(vm_obj.name))

        if len(new_ip) == 0 or len(gateway) == 0:
            errormsg = sys._getframe().f_code.co_filename, sys._getframe().f_code.co_name, sys._getframe().f_lineno, 'ip or gateway is None!'
            return {"bakc": "", "msg": errormsg}

        for device in vm_obj.config.hardware.device:
            if isinstance(device, vim.vm.device.VirtualVmxnet3) and device.deviceInfo.summary == vlan_name:
                nic_device = device
                break


        globalip = vim.vm.customization.GlobalIPSettings()
        adaptermap = vim.vm.customization.AdapterMapping()

        adaptermap.adapter = vim.vm.customization.IPSettings()
        adaptermap.macAddress = nic_device.macAddress
        adaptermap.adapter.dnsDomain = domain
        adaptermap.adapter.ip = vim.vm.customization.FixedIp(ipAddress=new_ip)
        adaptermap.adapter.subnetMask = netmask
        adaptermap.adapter.gateway = gateway
        globalip.dnsServerList = dns

        customspec = vim.vm.customization.Specification()
        identity = vim.vm.customization.LinuxPrep(domain=domain,
                                                  hostName=vim.vm.customization.FixedName(
                                                      name="kkx" + numm))
        customspec.identity = identity
        customspec.nicSettingMap = [adaptermap]

        customspec.globalIPSettings = globalip

        tasks = [vm_obj.CustomizeVM_Task(spec=customspec)]
        WaitForTasks(tasks, si)

        print(vm_obj.name, end="")
        print("修改IP完毕 ",numm)
        return {"back": True, "msg": ""}



    except Exception as e:
        errormsg = sys._getframe().f_code.co_filename, sys._getframe().f_code.co_name, sys._getframe().f_lineno
        if hasattr(e, 'msg'):
            msg = e.msg
            print (errormsg,msg)
            sys.exit(1)
        else:
            print ("the error is",errormsg, str(e))
            sys.exit(1)



def modify_ipmac(si,vm_obj,vlan_obj,domain,new_ip,netmask,dns,gateway,num):
    si = si
    vm_obj = vm_obj
    vlan_obj = vlan_obj

    if not vm_obj:
        errormsg = sys._getframe().f_code.co_filename, sys._getframe().f_code.co_name, sys._getframe().f_lineno
        raise Exception ("you must provide the vm_obj,",errormsg)


    if not vlan_obj:
        errormsg = sys._getframe().f_code.co_filename, sys._getframe().f_code.co_name, sys._getframe().f_lineno,"not get vlan_name"
        return {"back":"","msg":errormsg}

    if not si:
        errormsg = sys._getframe().f_code.co_filename, sys._getframe().f_code.co_name, sys._getframe().f_lineno,"not get si"
        return {"back": "", "msg": errormsg}


    try:
        if len(vlan_obj) == 1:

            print("判断虚拟机的状态：")

            while True:
                if vm_obj.summary.guest.toolsStatus == "toolsOk":
                    print("你好虚拟机正在运行，现在进行关闭虚拟机")
                    tasks = [vm_obj.PowerOff()]
                    WaitForTasks(tasks, si)
                    time.sleep(1)
                    break
                elif vm_obj.summary.guest.toolsStatus == "toolsNotRunning":
                    print("你好虚拟机正处于关闭状态:")
                    break

            vm_new_mac = randomMAC()
            vlan = vlan_obj[0]
            for device in vm_obj.config.hardware.device:
                if isinstance(device, vim.vm.device.VirtualEthernetCard) and device.deviceInfo.summary == vlan.name:
                    nic_device = device

            """修改mac地址,相当于手动编辑虚拟机，编辑设置-手动-修改MAC，系统的rules文件会自动增加一个mac配置信息"""

            virtual_nic_spec = vim.vm.device.VirtualDeviceSpec()
            virtual_nic_spec.operation = vim.vm.device.VirtualDeviceSpec.Operation.edit
            virtual_nic_spec.device = nic_device
            virtual_nic_spec.device.macAddress = vm_new_mac  ##最好和原来虚拟机存在的MAC不一致

            dev_changes = []
            dev_changes.append(virtual_nic_spec)
            config_mac = vim.vm.ConfigSpec()
            config_mac.deviceChange = dev_changes
            print("开始修改物理网卡地址:")
            print(vm_new_mac)
            tasks = [vm_obj.ReconfigVM_Task(spec=config_mac)]
            WaitForTasks(tasks, si)

            print("判断虚拟机的状态：")

            while True:
                if vm_obj.summary.guest.toolsStatus == "toolsOk":
                    print("你好虚拟机正在运行，现在进行关闭虚拟机")
                    tasks = [vm_obj.PowerOff()]
                    WaitForTasks(tasks, si)
                    time.sleep(1)
                    break
                elif vm_obj.summary.guest.toolsStatus == "toolsNotRunning":
                    print("你好虚拟机正处于关闭状态:")
                    break

            print("虚拟机已经关闭客户机，{}开始修改IP".format(vm_obj.name))

            if len(new_ip) == 0 or len(gateway) == 0:
                errormsg = sys._getframe().f_code.co_filename, sys._getframe().f_code.co_name, sys._getframe().f_lineno, 'ip or gateway is None!'
                return {"bakc": "", "msg": errormsg}

            globalip = vim.vm.customization.GlobalIPSettings()
            adaptermap = vim.vm.customization.AdapterMapping()

            adaptermap.adapter = vim.vm.customization.IPSettings()
            adaptermap.adapter.ip = vim.vm.customization.FixedIp(ipAddress=new_ip)
            adaptermap.adapter.subnetMask = netmask
            adaptermap.adapter.gateway = gateway
            globalip.dnsServerList = dns

            customspec = vim.vm.customization.Specification()
            identity = vim.vm.customization.LinuxPrep(hostName=vim.vm.customization.FixedName(name="kkx" + str(num)))
            customspec.identity = identity
            customspec.nicSettingMap = [adaptermap]
            customspec.globalIPSettings = globalip
            tasks = [vm_obj.CustomizeVM_Task(spec=customspec)]
            WaitForTasks(tasks, si)
            print(vm_obj.name, end="")
            print("修改IP完毕")
            tasks = [vm_obj.PowerOn()]
            WaitForTasks(tasks, si)

            return {"back": True, "msg": ""}


        elif len(vlan_obj) > 1:

            ip1 = "192.168.119.100"
            netmask1 = "255.255.255.0"
            gateway1 = "192.168.119.1"
            ip2 = "192.168.114.100"
            netmask2 = "255.255.255.0"
            gateway2 = "192.168.114.1"

            print("判断虚拟机的状态：")

            while True:
                if vm_obj.summary.guest.toolsStatus == "toolsOk":
                    print("你好虚拟机正在运行，现在进行关闭虚拟机")
                    tasks = [vm_obj.PowerOff()]
                    WaitForTasks(tasks, si)
                    time.sleep(1)
                    break
                elif vm_obj.summary.guest.toolsStatus == "toolsNotRunning":
                    print("你好虚拟机正处于关闭状态:")
                    break

            for vlan in vlan_obj:

                vm_new_mac = randomMAC()

                for device in vm_obj.config.hardware.device:
                    if isinstance(device, vim.vm.device.VirtualEthernetCard) and device.deviceInfo.summary == vlan.name:
                        nic_device = device

                """修改mac地址,相当于手动编辑虚拟机，编辑设置-手动-修改MAC，系统的rules文件会自动增加一个mac配置信息"""

                virtual_nic_spec = vim.vm.device.VirtualDeviceSpec()
                virtual_nic_spec.operation = vim.vm.device.VirtualDeviceSpec.Operation.edit
                virtual_nic_spec.device = nic_device
                virtual_nic_spec.device.macAddress = vm_new_mac  ##最好和原来虚拟机存在的MAC不一致

                dev_changes = []
                dev_changes.append(virtual_nic_spec)
                config_mac = vim.vm.ConfigSpec()
                config_mac.deviceChange = dev_changes
                print("开始修改物理网卡地址:")
                print(vm_new_mac)
                tasks = [vm_obj.ReconfigVM_Task(spec=config_mac)]
                WaitForTasks(tasks, si)
                print("修改物理网卡地址成功")
                time.sleep(1)
                tasks = [vm_obj.PowerOn()]
                WaitForTasks(tasks, si)
                """开始修改IP"""
                print("判断虚拟机的状态：")

                while True:
                    if vm_obj.summary.guest.toolsStatus == "toolsOk":
                        print("你好虚拟机正在运行，现在进行关闭虚拟机")
                        tasks = [vm_obj.PowerOff()]
                        WaitForTasks(tasks, si)
                        time.sleep(1)
                        break
                    elif vm_obj.summary.guest.toolsStatus == "toolsNotRunning":
                        break

                print("虚拟机已经关闭客户机，{}开始修改该物理网卡的IP".format(vm_obj.name))

                if len(new_ip) == 0 or len(gateway) == 0:
                    errormsg = sys._getframe().f_code.co_filename, sys._getframe().f_code.co_name, sys._getframe().f_lineno, 'ip or gateway is None!'
                    return {"bakc": "", "msg": errormsg}

                globalip = vim.vm.customization.GlobalIPSettings()
                adaptermap = vim.vm.customization.AdapterMapping()
                adaptermap.macAddress = virtual_nic_spec.device.macAddress
                adaptermap.adapter = vim.vm.customization.IPSettings()
                #
                # adaptermap.adapter.dnsDomain = domain
                adaptermap.adapter.ip = vim.vm.customization.FixedIp(ipAddress=ip1)
                adaptermap.adapter.subnetMask = names['netmask%s' % num]
                adaptermap.adapter.gateway = names['gateway%s' % num]
                globalip.dnsServerList = dns


                customspec = vim.vm.customization.Specification()
                identity = vim.vm.customization.LinuxPrep(hostName=vim.vm.customization.FixedName(name="kkx" + str(num)))
                customspec.identity = identity
                customspec.nicSettingMap = [adaptermap]
                customspec.globalIPSettings = globalip
                tasks = [vm_obj.CustomizeVM_Task(spec=customspec)]
                WaitForTasks(tasks, si)
                print(vm_obj.name, end="")
                print("修改IP完毕")
                tasks = [vm_obj.PowerOn()]
                WaitForTasks(tasks, si)

            return {"back": True, "msg": ""}

    except Exception as e:

        if hasattr(e, 'msg'):
            errormsg = sys._getframe().f_code.co_filename, sys._getframe().f_code.co_name, sys._getframe().f_lineno
            msg = e.msg
            print("have a error at:", errormsg, msg)
            sys.exit(1)
        else:
            errormsg = sys._getframe().f_code.co_filename, sys._getframe().f_code.co_name, sys._getframe().f_lineno
            print("the error is", errormsg, str(e))
            sys.exit(1)


def add_win_adapter(vm_obj,vlan_name,net_obj,si,domain,new_ip,netmask,dns,gateway,num):
    """增加网卡"""

    try:
        numm = str(rand_num(2))
        print("判断虚拟机的状态：")

        while True:
            if vm_obj.summary.guest.toolsStatus == "toolsOk":
                print("你好虚拟机正在运行，现在进行关闭虚拟机")
                tasks = [vm_obj.PowerOff()]
                WaitForTasks(tasks, si)
                time.sleep(1)
                break
            elif vm_obj.summary.guest.toolsStatus == "toolsNotRunning":
                break

        add_nic_spec = vim.vm.device.VirtualDeviceSpec()
        add_nic_spec.operation = vim.vm.device.VirtualDeviceSpec.Operation.add
        add_nic_spec.device = vim.vm.device.VirtualVmxnet3()
        add_nic_spec.device.wakeOnLanEnabled = True
        add_nic_spec.device.backing = vim.vm.device.VirtualEthernetCard.NetworkBackingInfo()
        add_nic_spec.device.backing.deviceName = vlan_name
        add_nic_spec.device.backing.network = net_obj  # jfj._get_obj(vim.Network, vlan_name)
        add_nic_spec.device.connectable = vim.vm.device.VirtualDevice.ConnectInfo()
        add_nic_spec.device.connectable.connected = True
        add_nic_spec.device.connectable.allowGuestControl = True
        add_nic_spec.device.connectable.startConnected =True

        add_netspec = []
        add_netspec.append(add_nic_spec)
        add_network = vim.vm.ConfigSpec()
        add_network.deviceChange = add_netspec

        print ("开始增加网卡")
        tasks = [vm_obj.ReconfigVM_Task(spec=add_network)]
        WaitForTasks(tasks,si)
        time.sleep(3)

        print("{}开始修改IP".format(vm_obj.name))

        globalip = vim.vm.customization.GlobalIPSettings()
        adaptermap = vim.vm.customization.AdapterMapping()

        adaptermap.adapter = vim.vm.customization.IPSettings()

        adaptermap.adapter.ip = vim.vm.customization.FixedIp()
        adaptermap.adapter.ip.ipAddress = new_ip
        adaptermap.adapter.subnetMask = netmask
        adaptermap.adapter.gateway = gateway
        globalip.dnsServerList = dns

        customspec = vim.vm.customization.Specification()
        identity = vim.vm.customization.Sysprep()
        identity.guiUnattended = vim.vm.customization.GuiUnattended()
        identity.guiUnattended.autoLogon = False
        identity.guiUnattended.autoLogonCount = 1
        identity.guiUnattended.password = vim.vm.customization.Password()
        identity.guiUnattended.password.value = "pass1234!@#"
        identity.guiUnattended.password.plainText = True
        identity.identification = vim.vm.customization.Identification()
        identity.userData = vim.vm.customization.UserData()
        identity.userData.fullName = "jfjtest"
        identity.userData.orgName = "jjtest"
        identity.userData.computerName = vim.vm.customization.FixedName(name="jfj" + numm)


        customspec.identity = identity
        customspec.nicSettingMap = [adaptermap]
        customspec.globalIPSettings = globalip
        tasks = [vm_obj.CustomizeVM_Task(spec=customspec)]
        WaitForTasks(tasks, si)
        print(vm_obj.name, end="")
        print("修改IP完毕", num)
        tasks = [vm_obj.PowerOn()]
        WaitForTasks(tasks, si)

        return {"back": True, "msg": ""}

    except Exception as e:
        errormsg = sys._getframe().f_code.co_filename, sys._getframe().f_code.co_name, sys._getframe().f_lineno
        if hasattr(e, 'msg'):
            msg = e.msg
            print (errormsg,msg)
            sys.exit(1)
        else:
            print ("the error is",errormsg, str(e))
            sys.exit(1)