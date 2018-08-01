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
        if host.name == "192.168.134.34":
            objView = content.viewManager.CreateContainerView(host,
                                                               [vim.ResourcePool],

                                                               True)
            vmList = objView.view
            objView.Destroy()

            for pool in vmList:
                if pool.name == "jfjqemu":
                    objView = content.viewManager.CreateContainerView(pool,
                                                                      [vim.VirtualMachine],

                                                                      True)
                    vmList = objView.view
                    objView.Destroy()
                    for vm in vmList:
                        if not vm.resourcePool is None:
                            try:
                                if vm.runtime.powerState == "poweredOff":
                                    vm.PowerOn()
                                else:
                                    print ("vm is not off status!")
                            except:
                                errormsg = sys._getframe().f_code.co_filename, sys._getframe().f_code.co_name, sys._getframe().f_lineno
                                print (errormsg)

if __name__ == "__main__":
    main()
    print("DOing all.....")