from pyVmomi import vim
import sys
sys.path.append("../clone_vm/")
import vm_clone_si as jvm


vm_list = ["ubuntu_server_host_pot_vmhost_template",
"ubuntu_server_host_pot_vmhost_template_mongodb",
"ubuntu_server_host_pot_vmhost_template_mysql",
"centos69_server_host_pot_vmhost_weblogic_template"]

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
                print(vm.runtime.host.name)



if __name__ == "__main__":
    main()
    print("DOing all.....")