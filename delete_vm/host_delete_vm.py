#coding=utf-8
from pyVmomi import vim
import sys,time
sys.path.append("../clone_vm/")
import vm_clone_si as jvm

def main():
    si,_ = jvm.get_vc_si()
    content = si.RetrieveServiceContent()
    objView = content.viewManager.CreateContainerView(content.rootFolder,
                                                      [vim.ComputeResource],
                                                      True)
    vmList = objView.view
    objView.Destroy()

    for host in vmList:
        if host.name == "192.168.134.21":
            objView = content.viewManager.CreateContainerView(host,
                                                              [vim.VirtualMachine],

                                                              True)
            vmList = objView.view
            objView.Destroy()
            for vm in vmList:
                print(vm.name)
                # vm.PowerOff()
                if not vm.resourcePool is None:
                    try:
                        if vm.runtime.powerState == "poweredOff":
                            vm.Destroy()
                            time.sleep(1)
                        else:
                            print("请先运行关闭虚拟机脚本，再来执行本程序")
                    except:
                        errormsg = sys._getframe().f_code.co_filename, sys._getframe().f_code.co_name, sys._getframe().f_lineno
                        print(errormsg)


if __name__ == "__main__":
    main()
    print("DOing all.....")