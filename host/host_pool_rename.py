#coding=utf-8
from pyVmomi import vim
import sys,atexit
import ssl
from pyVim.connect import SmartConnect, Disconnect

"""所有虚拟机名字减去一个字符"""
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
    host = "192.168.134.68"
    user = "root"
    password = "pass1234!@#$"
    port = 8081
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

def main():
    si = get_vc_si()
    content = si.RetrieveServiceContent()
    objView = content.viewManager.CreateContainerView(content.rootFolder,
                                                      [vim.ComputeResource],
                                                      True)
    vmList = objView.view
    objView.Destroy()

    for host in vmList:
        if host.name == "192.168.134.95":
            objView = content.viewManager.CreateContainerView(host,
                                                               [vim.ResourcePool],

                                                               True)
            vmList = objView.view
            objView.Destroy()

            for pool in vmList:
                if pool.name == "__three":
                    objView = content.viewManager.CreateContainerView(pool,
                                                                      [vim.VirtualMachine],

                                                                      True)
                    vmList = objView.view
                    objView.Destroy()
                    for vm in vmList:

                        #print(vm.name)
                        vm.Rename_Task(newName=vm.name[:-1])
                        #vm.Rename_Task(newName=vm.name+"backup")

if __name__ == "__main__":
    main()
    print("DOing all.....")