from pyVmomi import vim
import sys,re
sys.path.append("../clone_vm/")
import vm_clone_si as jvm


def main():
    si,_ = jvm.get_vc_si()
    content = si.RetrieveServiceContent()
    objView = content.viewManager.CreateContainerView(content.rootFolder,
                                                      [vim.Network],
                                                      True)
    vmList = objView.view
    objView.Destroy()

    for pool in vmList:
        if pool.name == "th is vlan225":
            print(pool)



if __name__ == "__main__":
    main()
    print("DOing all.....")