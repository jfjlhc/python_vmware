#coding=utf-8
from pyVmomi import vim
import sys,time
import vc_si as jvm


_host = "192.168.134.99"
_pool = "192.168.134.98_"

def main():
    si,_ = jvm.get_vc_si()
    content = si.RetrieveServiceContent()
    objView = content.viewManager.CreateContainerView(content.rootFolder,
                                                      [vim.ComputeResource],
                                                      True)
    vmList = objView.view
    objView.Destroy()

    for host in vmList:
        if host.name == _host:
            objView = content.viewManager.CreateContainerView(host,
                                                               [vim.ResourcePool],

                                                               True)
            vmList = objView.view
            objView.Destroy()

            for pool in vmList:
                if pool.name == _pool:
                    objView = content.viewManager.CreateContainerView(pool,
                                                                      [vim.VirtualMachine],

                                                                      True)
                    vmList = objView.view
                    objView.Destroy()
                    for vm in vmList:

                        if not vm.resourcePool is None:
                            try:
                                if vm.runtime.powerState == "poweredOff":
                                    vm.Destroy()
                                    time.sleep(1)
                                else:
                                    print ("请先运行关闭虚拟机脚本，再来执行本程序")
                            except:
                                errormsg = sys._getframe().f_code.co_filename, sys._getframe().f_code.co_name, sys._getframe().f_lineno
                                print (errormsg)

if __name__ == "__main__":
    main()
    print("DOing all.....")