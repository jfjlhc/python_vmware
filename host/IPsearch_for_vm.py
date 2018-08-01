from pyVmomi import vim
import sys, re

sys.path.append("../clone_vm/")
import vm_clone_si as jvm

"""through ip find vitrualmachine"""
def main():
    si, _ = jvm.get_vc_si()
    content = si.content
    objView = content.viewManager.CreateContainerView(content.rootFolder,
                                                      [vim.ComputeResource],
                                                      True)
    vmList = objView.view
    objView.Destroy()

    for i in vmList:
        if i.name == "192.168.134.236":
            objView = content.viewManager.CreateContainerView(i,
                                                               [vim.VirtualMachine],

                                                               True)
            vmList = objView.view
            objView.Destroy()
            obj = None
            for vm in vmList:
                if vm.name == "centos69_server_MS_userweb_svr_17.26_double_ipmac":
                    obj = vm

    objView = content.viewManager.CreateContainerView(content.rootFolder,
                                                      [vim.Datacenter],
                                                      True)
    vmList = objView.view
    objView.Destroy()
    data_obj = None
    for data in vmList:
        if data.name == "network":
            data_obj = data




    vmlist = content.searchIndex.FindByIp(datacenter=data_obj,ip="192.168.134.236",vmSearch=False)#find host_esxi
    #vmlist = content.searchIndex.FindByIp(datacenter=data_obj,ip="192.168.140.104",vmSearch=True)#find vm
    print(vmlist.name)


if __name__ == "__main__":
    main()
    print("DOing all.....")