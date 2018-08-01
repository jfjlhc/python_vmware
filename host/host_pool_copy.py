from pyVmomi import vim
import sys,time
sys.path.append("../clone_vm/")
import vc_si as jvm
import vm_clone_view as jview

b = jview.get_path("jfjjjj")

datastore =jview.get_object([vim.Datastore],'datat109')
resource_pool = jview.get_object([vim.ResourcePool],'HYA0003-13470-912_j')

relospec = vim.vm.RelocateSpec()
relospec.datastore =datastore
relospec.pool = resource_pool

spec1 = vim.vm.CloneSpec()
spec1.location = relospec
spec1.powerOn = False


def main():
    si,_ = jvm.get_vc_si()
    content = si.RetrieveServiceContent()
    objView = content.viewManager.CreateContainerView(content.rootFolder,
                                                      [vim.ComputeResource],
                                                      True)
    vmList = objView.view
    objView.Destroy()

    for host in vmList:
        if host.name == "192.168.134.236":
            objView = content.viewManager.CreateContainerView(host,
                                                               [vim.ResourcePool],

                                                               True)
            vmList = objView.view
            objView.Destroy()

            for pool in vmList:
                if pool.name == "jfj_network_1":
                    objView = content.viewManager.CreateContainerView(pool,
                                                                      [vim.VirtualMachine],

                                                                      True)
                    vmList = objView.view
                    objView.Destroy()
                    for vm in vmList:
                        vm.Clone(folder=b, name=vm.name + "j", spec=spec1)


if __name__ == "__main__":
    main()
    print("DOing all.....")