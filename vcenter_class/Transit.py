#coding=utf-8
from pyVim.connect import SmartConnect, Disconnect
import ssl
import sys
from pyVmomi import vim
sys.path.append("../")
from vcenter_class import mainfunc
from vcenter_class.kkx.variables import Variables

class Transit(object):
    def __init__(self,host,user,port,password):
        self.host = host
        self.user = user
        self.port = port
        self.password = password
        self.create_vcconnect()
        self.__content()
        self.args = Variables()

    def create_vcconnect(self):
        if self.host:
            self.context = ssl.create_default_context()
            self.context.check_hostname = False
            self.context.verify_mode = ssl.CERT_NONE
        else:
            if hasattr(ssl, '_create_unverified_context'):
                self.context = ssl._create_unverified_context()
        try:
            self._si = SmartConnect(host=self.host, user=self.user, pwd=self.password,
                                    port=self.port, sslContext=self.context)
        except Exception as e:
            print ("error is :",str(e))
            sys.exit(1)

    def close_vc(self):
        Disconnect(self._si)

    def __del__(self):
        self.close_vc()

    def __content(self):
        self._content = self._si.RetrieveServiceContent()

    def _get_obj(self,vimtype,obj_name):
        if vimtype == None or obj_name == None or len(obj_name)<=2:
            errormsg = sys._getframe().f_code.co_filename, sys._getframe().f_code.co_name, sys._getframe().f_lineno
            raise Exception (errormsg,"type is null or obj_name wrong")
            sys.exit(1)
        else:
            return mainfunc.get_obj(self._content,vimtype,obj_name)

    def _get_host(self):#获取所有主机对象
        if self._si == None or self._content == None:
            errormsg = sys._getframe().f_code.co_filename, sys._getframe().f_code.co_name, sys._getframe().f_lineno
            raise Exception (errormsg,"not get vc_si")
            sys.exit(1)
        else:
            return mainfunc.get_host(self._content)

    def _get_host_pool(self,hostname):#获取指定主机对象
        if hostname == None or hostname == "" or len(hostname) <= 2:
            errormsg = sys._getframe().f_code.co_filename, sys._getframe().f_code.co_name, sys._getframe().f_lineno
            raise Exception (errormsg,"hostname wrong")
        all_obj_list = self._get_host()
        return mainfunc.get_host_pool(self._content,all_obj_list,hostname)

    def _get_host_pool_vm(self,hostname,pool_name):#获取指定主机名，资源池下的虚拟机对象
        pool_obj_list = self._get_host_pool(hostname)
        return mainfunc.get_host_pool_vm(self._content,pool_obj_list,pool_name)

    def _get_vm_obj(self,vimtype,vm_name):
        try:
            #print (vm_name)
            if not vm_name:
                print ("Please submit the virtual machine name")
            back = mainfunc.get_obj(content=self._content,vimtype=vimtype,name=vm_name)
            return {"back":back,"errormsg":" "}
        except Exception as e:
            errormsg = sys._getframe().f_code.co_filename, sys._getframe().f_code.co_name, sys._getframe().f_lineno
            print (errormsg,str(e))
            sys.exit(1)


    def _get_vlan_obj(self,vm_obj,vlan_name,vm_new_name):
        vm = vm_obj
        vlan_name = vlan_name
        vm_new_name = vm_new_name

        try:
            if not vm_obj:
                back_obj = self._get_vm_obj(vimtype=vim.VirtualMachine,vm_name=vm_new_name)
                vm = back_obj.get("back")

            if len(vm.network) <= 1:
                print("network:",len(vm.network))
                network_obj = vm.network[0]
                return network_obj

            else:
                print("network:", len(vm.network))
                if not vlan_name:
                    vlan_name = vm.network[0].name
                for network_obj in vm.network:
                    if network_obj.name == "th is vlan225":
                        return network_obj

        except Exception as e:
            errormsg = sys._getframe().f_code.co_filename, sys._getframe().f_code.co_name, sys._getframe().f_lineno
            print ("can't got the network_obj,",str(e),"in",errormsg)

    def get_network(self,name):
        content = self._content
        objView = content.viewManager.CreateContainerView(content.rootFolder,
                                                          [vim.Network],
                                                          True)
        vmList = objView.view
        objView.Destroy()

        for net in vmList:
            #print(net)
            if net.name == name:
                obj = net
        return obj

    def _modify_ipmac(self,vm_obj,vm_new_name,vm_vlan_name,new_ip,netmask,gateway,num):

        domain = "jfj.com"
        dns = ["114.114.114.114"]
        netmask = self.args.vm_netmask
        vm_obj = vm_obj
        vm_new_name = vm_new_name
        vm_vlan_name = vm_vlan_name
        new_ip = new_ip
        netmask = netmask
        gateway = gateway
        num = num
        vlan_obj = []


        try:

            if not vm_obj or len(vm_new_name) <5:
                errormsg = sys._getframe().f_code.co_filename, sys._getframe().f_code.co_name, sys._getframe().f_lineno
                raise Exception (errormsg,"here not get vmobj")
            if not vm_new_name:
                return {"back":"","msg":"you must provide the vmname"}

            if len(vm_vlan_name) < 1:
                errormsg = sys._getframe().f_code.co_filename, sys._getframe().f_code.co_name, sys._getframe().f_lineno
                raise Exception(errormsg, "here not get vlan_name!")

            for i in vm_vlan_name.values():
                vm_vlan_name1 = self._get_vlan_obj(vm_obj, i, vm_new_name)
                vlan_obj.append(vm_vlan_name1)


            back_obj = mainfunc.modify_ipmac(self._si,vm_obj,vlan_obj,domain,new_ip,netmask,dns,gateway,num)

            if back_obj.get("back") == "":
                errormsg = sys._getframe().f_code.co_filename, sys._getframe().f_code.co_name, sys._getframe().f_lineno,"back_obj wrong"
                return {"back":"","msg":errormsg}
            return {"back":True,"msg":""}

        except Exception as e:
            errormsg = sys._getframe().f_code.co_filename, sys._getframe().f_code.co_name, sys._getframe().f_lineno
            if hasattr(e,"msg"):
                msg = e.msg
                print ("modify_mac error at:", errormsg,msg)
                sys.exit(1)

            else:
                print ("modify_mac error at:", errormsg,e)
                sys.exit(1)

    def _add_linux_adapder(self,vm_obj,vm_new_name,vm_vlan_name,new_ip,netmask,gateway,num):


        domain = "jfj.com"
        dns = ["114.114.114.114"]
        netmask = self.args.vm_netmask
        vm_obj = vm_obj
        new_ip = new_ip
        netmask = netmask
        gateway = gateway
        num = num

        net_obj = self._get_obj(vimtype=vim.Network, obj_name="th is vlan225")

        mainfunc.add_linux_adapter(vm_obj=vm_obj, vlan_name="th is vlan225", net_obj=net_obj, si=self._si, domain=domain,
                    new_ip=new_ip, netmask=netmask, dns=dns, gateway=gateway, num=num)
        return {"back": True, "msg": ""}

