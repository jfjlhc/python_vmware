from pyVmomi import vim
import sys,re
sys.path.append("../clone_vm/")
import vm_clone_si as jvm


def main():
    si = jvm.get_vc_si()
    content = si.RetrieveServiceContent()
    objView = content.viewManager.CreateContainerView(content.rootFolder,
                                                      [vim.ResourcePool],
                                                      True)
    vmList = objView.view
    objView.Destroy()

    for pool in vmList:
        print(pool.name)



if __name__ == "__main__":
    main()
    print("DOing all.....")