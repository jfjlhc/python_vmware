#coding=utf-8
from pyVmomi import vim
import sys,time
sys.path.append("../clone_vm/")
import vc_si as jvm

def main():
    si,_ = jvm.get_vc_si()
    content = si.RetrieveServiceContent()
    objView = content.viewManager.CreateContainerView(content.rootFolder,
                                                      [vim.ComputeResource],
                                                      True)
    vmList = objView.view
    objView.Destroy()

    for i in vmList:
        if i.name == "192.168.134.111":
            objView = content.viewManager.CreateContainerView(i,
                                                               [vim.VirtualMachine],

                                                               True)
            vmList = objView.view
            objView.Destroy()
            for vm in vmList:
                if not vm.resourcePool is None:
                    try:
                        if vm.runtime.powerState == "poweredOn":
                            if vm.guest.toolsVersionStatus == "guestToolsCurrent":
                                # if vm.name == "ros_192.168.134.100":
                                if vm.guest.toolsRunningStatus == "guestToolsRunning":
                                    vm.ShutdownGuest()
                                    time.sleep(3)
                                else:
                                    if vm.guest.toolsRunningStatus == "guestToolsNotRunning":
                                        vm.PowerOff()
                                        time.sleep(3)
                            elif vm.guest.toolsVersionStatus == "guestToolsNotInstalled":
                                vm.PowerOff()
                                time.sleep(1)
                            else:
                                print(vm.guest.toolsVersionStatus)
                                vm.PowerOff()
                    except:
                        vm.PowerOff()



if __name__ == "__main__":
    main()
    #print("所有虚拟机已经关闭了“)