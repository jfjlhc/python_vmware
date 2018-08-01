from pyVmomi import vim
import sys,re
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

    for i in vmList:
        if i.name == "192.168.134.121":
            objView2 = content.viewManager.CreateContainerView(i,
                                                               [vim.VirtualMachine],

                                                               True)
            vmList2 = objView2.view
            objView2.Destroy()
            obj = None
            for vm in vmList2:
                print(vm.name)



if __name__ == "__main__":
    main()
    print("DOing all.....")