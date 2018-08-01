from pyVmomi import vim
import sys
sys.path.append("../clone_vm/")
import vm_clone_view as jview
import vm_clone_si as jvm

b = jview.get_path("jfjjjj")

datastore =jview.get_object([vim.Datastore],'data104 (1)')
resource_pool = jview.get_object([vim.ResourcePool],'jfj_copy_pool')

relospec = vim.vm.RelocateSpec()
relospec.datastore =datastore
relospec.pool = resource_pool

spec1 = vim.vm.CloneSpec()
spec1.location = relospec
spec1.powerOn = False
spec1.template = True

vm_list = ["ubuntu_server_host_pot_vmhost_template_mysql"]

def main():
    si,_ = jvm.get_vc_si()
    content = si.RetrieveServiceContent()
    objView = content.viewManager.CreateContainerView(content.rootFolder,
                                                      [vim.VirtualMachine],
                                                      True)
    vmList = objView.view
    objView.Destroy()

    for vm in vmList:
        if vm.resourcePool is None:
            if vm.name in vm_list:
                vm.Clone(folder=b, name=vm.name + "_j", spec=spec1)



if __name__ == "__main__":
    main()
    print("DOing all.....")