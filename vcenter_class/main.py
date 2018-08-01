#coding=utf-8
import sys
from pyVmomi import vim
names = locals()
sys.path.append("../")
from vcenter_class.Transit import Transit
from vcenter_class.kkx.variables import Variables
from vcenter_class.mainfunc import WaitForTasks
import vcenter_class.mainfunc as mainfunc

"""Edit by  jifujun~~"""
""" my blog """

arg = Variables()
class Vcenter(object):

    def __init__(self,host,user,port,password):

        self.host = host
        self.user = user
        self.port = port
        self.password = password
        self.sendconnect = Transit(self.host,self.user,self.port,self.password)
        self.args = Variables()




    def linux_ipmac_modify(self,vm_obj,vm_new_name,vm_vlan_name,new_ip, netmask,gateway,num):##mac地址不可用的时候进入系统就会启动不了网卡



        try:
            if not vm_new_name:
                return {"back":"","msg":"not new_name"}

            if not vm_obj or vm_obj=="":
                back_obj = self.sendconnect._get_vm_obj(vim.VirtualMachine, vm_new_name)
                vm_obj = back_obj.get("back", "")

            if not vm_obj:
                return {"back":True,"msg":"not get vm_obj"}

            back_mac = self.sendconnect._modify_ipmac(vm_obj, vm_new_name, vm_vlan_name,new_ip,netmask,gateway,num)
            return {"back": True, "msg": ""}

        except Exception as e:
            errormsg = sys._getframe().f_code.co_filename, sys._getframe().f_code.co_name, sys._getframe().f_lineno
            print (errormsg,str(e))
            sys.exit(1)


    def rename_pool_vm(self):
        if not self.args.desc_host or not self.args.desc_pool:
            errormsg = sys._getframe().f_code.co_filename, sys._getframe().f_code.co_name, sys._getframe().f_lineno
            raise Exception (errormsg,"not host or pool")
        pool_obj = self.sendconnect._get_host_pool_vm(self.args.desc_host,self.args.desc_pool)
        return pool_obj




def deal_linux_ipmac(config):
    """批量修改linux的IP和mac地址"""
    jfj = Vcenter(host=arg.vcenter, user=arg.vc_user, port=443, password=arg.vc_passwd)

    try:
        num = 0
        for vm_dic in config:
            if len(vm_dic) == 0:
                continue
            num = num+1
            vm_obj = vm_dic.get("vm_obj", "")
            new_ip = vm_dic.get('guest_ip', "")
            netmask = vm_dic.get("netmask", "")
            gateway = vm_dic.get("gateway", "")
            vm_guest_name = vm_dic.get("guest_name", "")
            vm_new_name = vm_dic.get("new_name", "")
            vm_vlan_name = vm_dic.get("vlan", "")


            if not vm_guest_name or len(vm_guest_name) == 0:
                raise Exception("not get vm_name!")


            back_mac = jfj.linux_ipmac_modify(vm_obj=vm_obj, vm_new_name=vm_guest_name, vm_vlan_name=vm_vlan_name,new_ip=new_ip, netmask=netmask,gateway=gateway,num=num)

            if not back_mac.get("back", ""):
                errormsg = sys._getframe().f_code.co_filename, sys._getframe().f_code.co_name, sys._getframe().f_lineno
                raise Exception("{},modify_linux fail at:".format(vm_new_name), errormsg)

    except Exception as e:
        errormsg = sys._getframe().f_code.co_filename, sys._getframe().f_code.co_name, sys._getframe().f_lineno
        print (errormsg,str(e))
        sys.exit(1)


def linux_ipmac(config):
    """批量修改linux的IP和mac地址,del network"""
    jfj = Vcenter(host=arg.vcenter, user=arg.vc_user, port=443, password=arg.vc_passwd)

    try:
        num = 0
        for vm_dic in config:
            if len(vm_dic) == 0:
                continue
            num = num+1
            vm_obj = vm_dic.get("vm_obj", "")
            new_ip = vm_dic.get('guest_ip', "")
            netmask = vm_dic.get("netmask", "")
            gateway = vm_dic.get("gateway", "")
            vm_guest_name = vm_dic.get("guest_name", "")
            vm_new_name = vm_dic.get("guest_name", "")
            vm_vlan_name = vm_dic.get("vlan", "")
            vlan_obj = []
            domain = "jfj.com"
            dns = ["114.114.114.114"]

            if not vm_obj or vm_obj=="":
                back_obj = jfj.sendconnect._get_vm_obj(vim.VirtualMachine,vm_new_name)
                vm_obj = back_obj.get("back", "")

            """先删除网卡"""
            del_nic = mainfunc.delete_adapter(vm=vm_obj,si=jfj.sendconnect._si)

            """再增加网卡配置ip"""

            if len(vm_vlan_name) == 1:

                vlan_name = vm_vlan_name['1']
                net_obj = jfj.sendconnect._get_obj(vimtype=vim.Network, obj_name=vlan_name)
                mainfunc.add_linux_adapter(vm_obj, vlan_name, net_obj, jfj.sendconnect._si, domain, new_ip, netmask,dns, gateway, num)
                tasks = [vm_obj.PowerOn()]
                WaitForTasks(tasks, jfj.sendconnect._si)


            if len(vm_vlan_name) > 1:

                vlan_name = vm_vlan_name['1']
                net_obj = jfj.sendconnect._get_obj(vimtype=vim.Network, obj_name=vlan_name)
                mainfunc.add_linux_adapter(vm_obj, vlan_name, net_obj, jfj.sendconnect._si, domain, new_ip, netmask,dns, gateway, num)

                vlan_name = vm_vlan_name['2']
                #mainfunc.add_linux_adapter(vm_obj, vlan_name, net_obj, jfj.sendconnect._si, domain, new_ip, netmask,dns, gateway, num)
                mainfunc.add_adapter(vm_obj, vlan_name, net_obj, jfj.sendconnect._si)
                tasks = [vm_obj.PowerOn()]
                WaitForTasks(tasks, jfj.sendconnect._si)

            print("第{}个虚拟机修改完毕".format(num))

    except Exception as e:
        errormsg = sys._getframe().f_code.co_filename, sys._getframe().f_code.co_name, sys._getframe().f_lineno
        print (errormsg,str(e))
        sys.exit(1)



def deal_win_ipmac(config):
    """批量修改windows的IP和mac地址"""
    jfj = Vcenter(host=arg.vcenter, user=arg.vc_user, port=443, password=arg.vc_passwd)

    try:
        num = 0
        for vm_dic in config:
            if len(vm_dic) == 0:
                continue
            num = num+1
            vm_obj = vm_dic.get("vm_obj", "")
            new_ip = vm_dic.get('guest_ip', "")
            netmask = vm_dic.get("netmask", "")
            gateway = vm_dic.get("gateway", "")
            vm_guest_name = vm_dic.get("guest_name", "")
            vm_new_name = vm_dic.get("guest_name", "")
            vm_vlan_name = vm_dic.get("vlan", "")
            vlan_obj = []
            domain = "jfj.com"
            dns = ["114.114.114.114"]

            if not vm_obj or vm_obj=="":
                back_obj = jfj.sendconnect._get_vm_obj(vim.VirtualMachine,vm_new_name)
                vm_obj = back_obj.get("back", "")

            """先删除网卡"""
            del_nic = mainfunc.delete_adapter(vm=vm_obj,si=jfj.sendconnect._si)

            """再增加网卡配置ip"""

            for vlan_names in vm_vlan_name.values():
                net_obj = jfj.sendconnect._get_obj(vimtype=vim.Network, obj_name=vlan_names)
                mainfunc.add_win_adapter(vm_obj, vlan_names, net_obj, jfj.sendconnect._si, domain, new_ip, netmask, dns, gateway, num)

    except Exception as e:
        errormsg = sys._getframe().f_code.co_filename, sys._getframe().f_code.co_name, sys._getframe().f_lineno
        print (errormsg,str(e))
        sys.exit(1)

def manager_linux_adapder(config):
    """增加单个网卡"""
    jfj = Vcenter(host=arg.vcenter, user=arg.vc_user, port=443, password=arg.vc_passwd)

    try:
        num = 0
        for vm_dic in config:
            if len(vm_dic) == 0:
                continue
            num = num + 1
            vm_obj = vm_dic.get("vm_obj", "")
            new_ip = vm_dic.get('guest_ip', "")
            netmask = vm_dic.get("netmask", "")
            gateway = vm_dic.get("gateway", "")
            vm_guest_name = vm_dic.get("guest_name", "")
            vm_new_name = vm_dic.get("guest_name", "")
            vm_vlan_name = vm_dic.get("vlan", "")

            if not vm_guest_name or len(vm_guest_name) == 0:
                raise Exception("not get vm_name!")


            if not vm_obj or vm_obj=="":
                back_obj = jfj.sendconnect._get_vm_obj(vim.VirtualMachine,vm_new_name)
                vm_obj = back_obj.get("back", "")

            back_add = jfj.sendconnect._add_linux_adapder(vm_obj, vm_new_name, vm_vlan_name, new_ip, netmask, gateway, num)
            return {"back": True, "msg": ""}

    except Exception as e:
        errormsg = sys._getframe().f_code.co_filename, sys._getframe().f_code.co_name, sys._getframe().f_lineno
        print(errormsg, str(e))
        sys.exit(1)





def config_dic():
    """Generate a dictionary"""

    jfj = Vcenter(host=arg.vcenter, user=arg.vc_user, port=443, password=arg.vc_passwd)
    vmList = jfj.sendconnect._get_host_pool_vm(hostname=arg.desc_host,pool_name=arg.desc_pool)
    vmguest = []
    esxi_vm = []
    num = 0

    for vm in vmList:
        vmguest.append(vm.name)

    for obj_name in vmguest:
        #name = rand_char_str(5)
        num = num + 1
        names['dic%s' % num]={}

        if obj_name == arg.vm_1th and arg.vm_1th in vmguest:
            names['dic%s' % num]['guest_name'] = obj_name
            names['dic%s' % num]['netmask'] = arg.vm_netmask
            names['dic%s' % num]['guest_ip'] = arg.vm_1th_ip
            names['dic%s' % num]['gateway'] = arg.vm_1th_gw
            names['dic%s' % num]['vlan'] = arg.vm_1th_vlan

        elif obj_name == arg.vm_2th and arg.vm_2th in vmguest:
            names['dic%s' % num]['guest_name'] = obj_name
            names['dic%s' % num]['netmask'] = arg.vm_netmask
            names['dic%s' % num]['guest_ip'] = arg.vm_2th_ip
            names['dic%s' % num]['gateway'] = arg.vm_2th_gw
            names['dic%s' % num]['vlan'] = arg.vm_2th_vlan

        elif obj_name == arg.vm_3th and arg.vm_3th in vmguest:
            names['dic%s' % num]['guest_name'] = obj_name
            names['dic%s' % num]['netmask'] = arg.vm_netmask
            names['dic%s' % num]['guest_ip'] = arg.vm_3th_ip
            names['dic%s' % num]['gateway'] = arg.vm_3th_gw
            names['dic%s' % num]['vlan'] = arg.vm_3th_vlan

        elif obj_name == arg.vm_4th and arg.vm_4th in vmguest:
            names['dic%s' % num]['guest_name'] = obj_name
            names['dic%s' % num]['netmask'] = arg.vm_netmask
            names['dic%s' % num]['guest_ip'] = arg.vm_4th_ip
            names['dic%s' % num]['gateway'] = arg.vm_4th_gw
            names['dic%s' % num]['vlan'] = arg.vm_1th_vlan

        elif obj_name == arg.vm_5th and arg.vm_5th in vmguest:
            names['dic%s' % num]['guest_name'] = obj_name
            names['dic%s' % num]['netmask'] = arg.vm_netmask
            names['dic%s' % num]['guest_ip'] = arg.vm_5th_ip
            names['dic%s' % num]['gateway'] = arg.vm_5th_gw
            names['dic%s' % num]['vlan'] = arg.vm_5th_vlan

        elif obj_name == arg.vm_6th and arg.vm_6th in vmguest:
            names['dic%s' % num]['guest_name'] = obj_name
            names['dic%s' % num]['netmask'] = arg.vm_netmask
            names['dic%s' % num]['guest_ip'] = arg.vm_6th_ip
            names['dic%s' % num]['gateway'] = arg.vm_6th_gw
            names['dic%s' % num]['vlan'] = arg.vm_6th_vlan

        elif obj_name == arg.vm_7th and arg.vm_7th in vmguest:
            names['dic%s' % num]['guest_name'] = obj_name
            names['dic%s' % num]['netmask'] = arg.vm_netmask
            names['dic%s' % num]['guest_ip'] = arg.vm_7th_ip
            names['dic%s' % num]['gateway'] = arg.vm_7th_gw
            names['dic%s' % num]['vlan'] = arg.vm_1th_vlan

        elif obj_name == arg.vm_8th and arg.vm_8th in vmguest:
            names['dic%s' % num]['guest_name'] = obj_name
            names['dic%s' % num]['netmask'] = arg.vm_netmask
            names['dic%s' % num]['guest_ip'] = arg.vm_8th_ip
            names['dic%s' % num]['gateway'] = arg.vm_8th_gw
            names['dic%s' % num]['vlan'] = arg.vm_8th_vlan

        elif obj_name == arg.vm_9th and arg.vm_9th in vmguest:
            names['dic%s' % num]['guest_name'] = obj_name
            names['dic%s' % num]['netmask'] = arg.vm_netmask
            names['dic%s' % num]['guest_ip'] = arg.vm_9th_ip
            names['dic%s' % num]['gateway'] = arg.vm_9th_gw
            names['dic%s' % num]['vlan'] = arg.vm_9th_vlan

        elif obj_name == arg.vm_10th and arg.vm_10th in vmguest:
            names['dic%s' % num]['guest_name'] = obj_name
            names['dic%s' % num]['netmask'] = arg.vm_netmask
            names['dic%s' % num]['guest_ip'] = arg.vm_10th_ip
            names['dic%s' % num]['gateway'] = arg.vm_10th_gw
            names['dic%s' % num]['vlan'] = arg.vm_10th_vlan

        elif obj_name == arg.vm_11th and arg.vm_11th in vmguest:
            names['dic%s' % num]['guest_name'] = obj_name
            names['dic%s' % num]['netmask'] = arg.vm_netmask
            names['dic%s' % num]['guest_ip'] = arg.vm_11th_ip
            names['dic%s' % num]['gateway'] = arg.vm_11th_gw
            names['dic%s' % num]['vlan'] = arg.vm_11th_vlan

        elif obj_name == arg.vm_12th and arg.vm_12th in vmguest:
            names['dic%s' % num]['guest_name'] = obj_name
            names['dic%s' % num]['netmask'] = arg.vm_netmask
            names['dic%s' % num]['guest_ip'] = arg.vm_12th_ip
            names['dic%s' % num]['gateway'] = arg.vm_12th_gw
            names['dic%s' % num]['vlan'] = arg.vm_12th_vlan

        elif obj_name == arg.vm_13th and arg.vm_13th in vmguest:
            names['dic%s' % num]['guest_name'] = obj_name
            names['dic%s' % num]['netmask'] = arg.vm_netmask
            names['dic%s' % num]['guest_ip'] = arg.vm_13th_ip
            names['dic%s' % num]['gateway'] = arg.vm_13th_gw
            names['dic%s' % num]['vlan'] = arg.vm_13th_vlan

        elif obj_name == arg.vm_14th and arg.vm_14th in vmguest:
            names['dic%s' % num]['guest_name'] = obj_name
            names['dic%s' % num]['netmask'] = arg.vm_netmask
            names['dic%s' % num]['guest_ip'] = arg.vm_14th_ip
            names['dic%s' % num]['gateway'] = arg.vm_14th_gw
            names['dic%s' % num]['vlan'] = arg.vm_14th_vlan

        elif obj_name == arg.vm_15th and arg.vm_15th in vmguest:
            names['dic%s' % num]['guest_name'] = obj_name
            names['dic%s' % num]['netmask'] = arg.vm_netmask
            names['dic%s' % num]['guest_ip'] = arg.vm_15th_ip
            names['dic%s' % num]['gateway'] = arg.vm_15th_gw
            names['dic%s' % num]['vlan'] = arg.vm_15th_vlan

        elif obj_name == arg.vm_16th and arg.vm_16th in vmguest:
            names['dic%s' % num]['guest_name'] = obj_name
            names['dic%s' % num]['netmask'] = arg.vm_netmask
            names['dic%s' % num]['guest_ip'] = arg.vm_16th_ip
            names['dic%s' % num]['gateway'] = arg.vm_16th_gw
            names['dic%s' % num]['vlan'] = arg.vm_16th_vlan
        esxi_vm.append(names['dic%s' % num])

    return esxi_vm



def modify_ip_mac():

    array = config_dic()
    print(array)
    deal_linux_ipmac(array)#修改linux IP和mac
    #deal_win_ipmac(array)#先删除网卡再增加网卡配置IP和MAC
    #linux_ipmac(array)


def rename_vm():

    jfj = Vcenter(host=arg.vcenter, user=arg.vc_user, port=443, password=arg.vc_passwd)
    pool = jfj.rename_pool_vm()
    num =0
    for vm in pool:
        num +=1
        name = "network_route"+str(num)+"_j"
        vm.Rename_Task(newName=name)



if __name__ == "__main__":
    modify_ip_mac()
