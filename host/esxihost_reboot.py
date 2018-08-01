from pyVmomi import vim
import sys
sys.path.append("../")
import vc_si as jvm


def main():
    si,context = jvm.get_vc_si()
    content = si.RetrieveServiceContent()
    objView = content.viewManager.CreateContainerView(content.rootFolder,
                                                      [vim.ComputeResource],
                                                      True)
    vmList = objView.view
    objView.Destroy()


    for i in vmList:
        if i.name == "192.168.134.21":
            i.host[0].RebootHost_Task(force=True)

if __name__ == "__main__":
    main()
    print("DOing all.....")