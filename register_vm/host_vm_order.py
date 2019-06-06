# -*- coding: utf-8 -*-
#/usr/bin/env python

from pyVmomi import vim
"""设置虚拟机启动顺序，要是不生效的，becasue 名字不合法"""

g_vms = {'ros_1.1.1.157%2f192.168.75.157%2f192.168.134.68': 1,
         'vCenter-1.1.1.150%2f192.168.75.150': 2,
         'ntp_1.1.1.101': 3,
         'cs69_SF_share_dir_svr_1.1.1.25': 4,
         'cs69_system_admin_server_1.1.1.66%2f192.168.75.2': 5,
         'cs69_MS_userweb_svr_1.1.1.36': 6,
         'cs69_MS_userweb_svr_1.1.1.26%2f192.168.75.26': 7,
         'cs69_DC_data_collect_1.1.1.20%2f192.168.75.20': 8,
         'cs69_MS_data_process_1.1.1.22': 9,
         'cs69_DM_deploy_svr_1.1.1.21%2f192.168.75.21': 10,
         'cs69_DM_deploy_vmwareagent_1.1.1.28': 11,
         'ub14_DM_alarmpot_dockerhost_1.1.1.24%2f192.168.75.24' :12,
         'cs7_gateway_1.1.1.30%2f192.168.75.30%2f192.168.77.1': 13,
         'ub14_flowdump_1.1.1.31': 14,
         '7pRasKetXLQZ': 15,
         'DE7KAzZ8fapT': 16,
         'xBmSfXtCARca': 17,
         'X5PtJN7U6Doq': 18,
         'YAc9yr85I2V3': 19,
         'fwdKbRUN6egl': 20,
         'AxnJfM53BSYl': 21,
         'B9UJ2g1XfrhV': 22,
         'WCdpIKYTyUAz': 23,
         'K7aRMx1ObWBo': 24,
         '12D634iQysWv': 25,
         'W3KxkpMiAwBH': 26,
         'l2TgkQmwWIHi': 27,
         'yQrdpwoYb1tT': 28,
         'CqmniIfbrkhy': 29,
         'tEaQswi7pSK9': 30,
         'rfNYIi8zjgq4': 31,
         'tmBSsaHKNY7A': 32,
         'f67psIkacLjv': 33,
         'CE9XUhy8xJaD': 34,
         'kv8j0w2yLGNX': 35,
         'a3mjVUCXhQxp': 36,



         }


def _get_obj(content, vimtype, name):
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


def get_host_by_name(si):
    """
    Find a virtual machine by it's name and return it
    """
    host_obj = si.RetrieveContent().rootFolder.childEntity[0].hostFolder.childEntity[0].host[0]
    return host_obj


def get_vm_by_name(si, name):
    """
    Find a virtual machine by it's name and return it
    """
    return _get_obj(si.RetrieveContent(), [vim.VirtualMachine], name)


def _enable_auto_restart(si, host_obj, vm_obj):
    try:

        hostDefSettings = vim.host.AutoStartManager.SystemDefaults()
        hostDefSettings.enabled = True
        hostDefSettings.startDelay = 30

        spec = host_obj.configManager.autoStartManager.config
        spec.defaults = hostDefSettings
        auto_power_info = vim.host.AutoStartManager.AutoPowerInfo()
        auto_power_info.key = vm_obj

        auto_power_info.startAction = 'powerOn'
        auto_power_info.stopAction = 'None'
        auto_power_info.stopDelay = -1
        auto_power_info.waitForHeartbeat = 'no'

        if vm_obj.name == 'ros_1.1.1.157%2f192.168.75.157%2f192.168.134.68':

            auto_power_info.startOrder = 1
            auto_power_info.startDelay = 30

        elif vm_obj.name == 'vCenter-1.1.1.150%2f192.168.75.150':

            auto_power_info.startOrder = 2
            auto_power_info.startDelay = 60

        elif vm_obj.name == 'ntp_1.1.1.101':

            auto_power_info.startOrder = 3
            auto_power_info.startDelay = 30

        elif vm_obj.name == 'cs69_SF_share_dir_svr_1.1.1.25':

            auto_power_info.startOrder = 4
            auto_power_info.startDelay = 60

        elif vm_obj.name == 'cs69_system_admin_server_1.1.1.66%2f192.168.75.2':

            auto_power_info.startOrder = 5
            auto_power_info.startDelay = 30

        elif vm_obj.name == 'cs69_MS_userweb_svr_1.1.1.36':

            auto_power_info.startOrder = 6
            auto_power_info.startDelay = 120

        elif vm_obj.name == 'cs69_MS_userweb_svr_1.1.1.26%2f192.168.75.26':

            auto_power_info.startOrder = 7
            auto_power_info.startDelay = 60

        elif vm_obj.name == 'cs69_DC_data_collect_1.1.1.20%2f192.168.75.20':

            auto_power_info.startOrder = 8
            auto_power_info.startDelay = 240



        elif vm_obj.name == 'cs69_MS_data_process_1.1.1.22':

            auto_power_info.startOrder = 9
            auto_power_info.startDelay = 20

        elif vm_obj.name == 'cs69_DM_deploy_svr_1.1.1.21%2f192.168.75.21':

            auto_power_info.startOrder = 10
            auto_power_info.startDelay = 240



        elif vm_obj.name == 'cs69_DM_deploy_vmwareagent_1.1.1.28':

            auto_power_info.startOrder = 11
            auto_power_info.startDelay = 10

        elif vm_obj.name == 'ub14_DM_alarmpot_dockerhost_1.1.1.24%2f192.168.75.24':

            auto_power_info.startOrder = 12
            auto_power_info.startDelay = 10

        elif vm_obj.name == 'cs7_gateway_1.1.1.30%2f192.168.75.30%2f192.168.77.1':

            auto_power_info.startOrder = 13
            auto_power_info.startDelay = 10

        elif vm_obj.name == 'ub14_flowdump_1.1.1.31':

            auto_power_info.startOrder = 14
            auto_power_info.startDelay = 10

        elif vm_obj.name == '7pRasKetXLQZ':

            auto_power_info.startOrder = -1
            auto_power_info.startDelay = 10
            auto_power_info.startAction = 'PowerOn'

        elif vm_obj.name == 'DE7KAzZ8fapT':

            auto_power_info.startOrder = -1
            auto_power_info.startDelay = 10
            auto_power_info.startAction = 'PowerOn'

        elif vm_obj.name == 'xBmSfXtCARca':

            auto_power_info.startOrder = -1
            auto_power_info.startDelay = 10
            auto_power_info.startAction = 'PowerOn'

        elif vm_obj.name == 'X5PtJN7U6Doq':

            auto_power_info.startOrder = -1
            auto_power_info.startDelay = 10
            auto_power_info.startAction = 'PowerOn'

        elif vm_obj.name == 'YAc9yr85I2V3':

            auto_power_info.startOrder = -1
            auto_power_info.startDelay = 10
            auto_power_info.startAction = 'PowerOn'

        elif vm_obj.name == 'fwdKbRUN6egl':

            auto_power_info.startOrder = -1
            auto_power_info.startDelay = 10
            auto_power_info.startAction = 'PowerOn'

        elif vm_obj.name == 'AxnJfM53BSYl':

            auto_power_info.startOrder = -1
            auto_power_info.startDelay = 10
            auto_power_info.startAction = 'PowerOn'

        elif vm_obj.name == 'B9UJ2g1XfrhV':

            auto_power_info.startOrder = -1
            auto_power_info.startDelay = 10
            auto_power_info.startAction = 'PowerOn'



        elif vm_obj.name == 'WCdpIKYTyUAz':

            auto_power_info.startOrder = -1
            auto_power_info.startDelay = 10
            auto_power_info.startAction = 'PowerOn'

        elif vm_obj.name == 'K7aRMx1ObWBo':

            auto_power_info.startOrder = -1
            auto_power_info.startDelay = 10
            auto_power_info.startAction = 'PowerOn'

        elif vm_obj.name == '12D634iQysWv':

            auto_power_info.startOrder = -1
            auto_power_info.startDelay = 10
            auto_power_info.startAction = 'PowerOn'

        elif vm_obj.name == 'W3KxkpMiAwBH':

            auto_power_info.startOrder = -1
            auto_power_info.startDelay = 10
            auto_power_info.startAction = 'PowerOn'

        elif vm_obj.name == 'l2TgkQmwWIHi':

            auto_power_info.startOrder = -1
            auto_power_info.startDelay = 10
            auto_power_info.startAction = 'PowerOn'

        elif vm_obj.name == 'yQrdpwoYb1tT':

            auto_power_info.startOrder = -1
            auto_power_info.startDelay = 10
            auto_power_info.startAction = 'PowerOn'

        elif vm_obj.name == 'CqmniIfbrkhy':

            auto_power_info.startOrder = -1
            auto_power_info.startDelay = 10
            auto_power_info.startAction = 'PowerOn'

        elif vm_obj.name == 'tEaQswi7pSK9':

            auto_power_info.startOrder = -1
            auto_power_info.startDelay = 10
            auto_power_info.startAction = 'PowerOn'

        elif vm_obj.name == 'rfNYIi8zjgq4':

            auto_power_info.startOrder = -1
            auto_power_info.startDelay = 10
            auto_power_info.startAction = 'PowerOn'

        elif vm_obj.name == 'tmBSsaHKNY7A':

            auto_power_info.startOrder = -1
            auto_power_info.startDelay = 10
            auto_power_info.startAction = 'PowerOn'

        elif vm_obj.name == 'f67psIkacLjv':

            auto_power_info.startOrder = -1
            auto_power_info.startDelay = 10
            auto_power_info.startAction = 'PowerOn'

        elif vm_obj.name == 'CE9XUhy8xJaD':

            auto_power_info.startOrder = -1
            auto_power_info.startDelay = 10
            auto_power_info.startAction = 'PowerOn'

        elif vm_obj.name == 'kv8j0w2yLGNX':

            auto_power_info.startOrder = -1
            auto_power_info.startDelay = 10
            auto_power_info.startAction = 'PowerOn'

        elif vm_obj.name == 'a3mjVUCXhQxp':

            auto_power_info.startOrder = -1
            auto_power_info.startDelay = 10
            auto_power_info.startAction = 'PowerOn'

        spec.powerInfo = [auto_power_info]

        host_obj.configManager.autoStartManager.ReconfigureAutostart(spec)


    except Exception as e:
        print(e.msg)


def enable_auto_restart(si):
    try:


        host_obj = get_host_by_name(si)

        if not isinstance(host_obj, vim.HostSystem):
            return {'ret': False, 'desc': 'get_host_obj_failed'}

        def function1(x):
            return x[1]

        sort_vms = sorted(g_vms.items(), key=function1, reverse=False)#False顺序从小到大
        # print(sort_vms)
        # print()
        for sort_vm in sort_vms:

            vm_obj = get_vm_by_name(si, sort_vm[0])
            #print(vm_obj.name)
            if not isinstance(vm_obj, vim.VirtualMachine):
                print("get obj is not a vm!")


            _enable_auto_restart(si, host_obj, vm_obj)

    except Exception as e:
        print(e)



def create_vcenter_si():
    vcenter_ip = '192.168.134.98'
    vcenter_user = 'root'
    vcenter_pwd = 'pass1234!@#$'
    vcenter_port = 443
    si = None

    import ssl
    from pyVim import connect
    import atexit
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE

    try:
        si = connect.SmartConnect(host=vcenter_ip, user=vcenter_user, pwd=vcenter_pwd,
                                  port=vcenter_port, sslContext=ssl_context)
        atexit.register(connect.Disconnect, si)
    except Exception as e:
        print(str(e))
    return si


if __name__ == '__main__':
    si = create_vcenter_si()
    #print(si)
    enable_auto_restart(si)
    # get_host_by_name(si)