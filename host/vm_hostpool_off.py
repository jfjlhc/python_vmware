from pyVmomi import vim
import time
import vc_si as jvm


def main():
    si,_ = jvm.get_vc_si()
    content = si.RetrieveServiceContent()
    objView = content.viewManager.CreateContainerView(content.rootFolder,
                                                      [vim.ComputeResource],
                                                      True)
    vmList = objView.view
    objView.Destroy()

    for host in vmList:
        if host.name == "192.168.134.99":
            objView = content.viewManager.CreateContainerView(host,
                                                               [vim.ResourcePool],

                                                               True)
            vmList = objView.view
            objView.Destroy()

            for pool in vmList:
                if pool.name == "192.168.134.98_":
                    objView = content.viewManager.CreateContainerView(pool,
                                                                      [vim.VirtualMachine],

                                                                      True)
                    vmList = objView.view
                    objView.Destroy()
                    for vm in vmList:
                        if not vm.resourcePool is None:
                            try:
                                if vm.runtime.powerState == "poweredOn":
                                    if vm.guest.toolsVersionStatus == "guestToolsCurrent":
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
                                else:
                                    print ("vm is already in poweroff")
                            except:
                                vm.PowerOff()

if __name__ == "__main__":
    main()
    print("DOing all.....")