#!/usr/bin/env python
import sys
sys.path.append("../clone_vm")
import vm_clone_view as jview
from pyVmomi import vim, vmodl
import vm_clone_si as jvm

b = jview.get_path("jfjjjj")

datastore =jview.get_object([vim.Datastore],'datastore95')
resource_pool = jview.get_object([vim.ResourcePool],'__three')

relospec = vim.vm.RelocateSpec()
relospec.datastore =datastore
relospec.pool = resource_pool

spec1 = vim.vm.CloneSpec()
spec1.location = relospec
spec1.powerOn = False


def main():
    si = None
    si,_ = jvm.get_vc_si()
    content = si.RetrieveServiceContent()
    objView = content.viewManager.CreateContainerView(content.rootFolder,
                                                      [vim.ComputeResource],
                                                      True)
    vmList = objView.view
    objView.Destroy()

    for host in vmList:
        if host.name == "192.168.134.121":
            objView = content.viewManager.CreateContainerView(host,
                                                               [vim.VirtualMachine],

                                                               True)
            vmList = objView.view
            objView.Destroy()
            for vm in vmList:
                vm.Clone(folder=b, name=vm.name + "_h", spec=spec1)

if __name__ == "__main__":
    main()
    print("DOing all.....")