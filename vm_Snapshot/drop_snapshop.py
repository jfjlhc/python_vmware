from pyVmomi import vim
import sys
sys.path.append("../clone_vm/")
import vm_clone_si as jvm
from pyVmomi import vim
import sys,atexit
import ssl
from pyVim.connect import SmartConnect, Disconnect



def set_vc_si(host,user,port,password,context):
    try:
        si1 = SmartConnect(host=host, user=user,pwd=password,
                          port=port, sslContext=context)
        if not si1:
            print ("Can't connect to the host with given user and password")
            sys.exit()

        atexit.register(Disconnect, si1)


    except Exception as e:
        print ("catch the exception: ", str(e))
    return si1




def get_vc_si():
    host = "192.168.134.107"
    user = "root"
    password = "pass1234!@#$"
    port = 443
    if host:
        context = ssl.create_default_context()
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE
    else:
        if hasattr(ssl, '_create_unverified_context'):
            context = ssl._create_unverified_context()


    si = set_vc_si(host, user, port, password, context)
    atexit.register(Disconnect, si)
    return si

def Drop_snap(resourcePool):
    try:
        if resourcePool.name == "Hy_Os":
            name = "jfjnew"
            for vm in resourcePool.vm:
                name = name + "1"
                vm.snapshot.currentSnapshot.Remove(removeChildren=False)##remove all snap == vm.RemoveAllSnapshots()
                #vm.RemoveAllSnapshots()
    except Exception as e:
        print("no have this name :", str(e))


def wait_for_task(task):
    task_do = False
    while not task_do:
        if task.info.state == "success":
            return task.info.result
        if task.info.state == "error":
            print("There has an error :")
            task_do = True




def main():
    si = get_vc_si()
    content = si.RetrieveServiceContent()
    objView = content.viewManager.CreateContainerView(content.rootFolder,
                                                      [vim.ResourcePool],
                                                      True)
    vmList = objView.view
    objView.Destroy()
    for i in vmList:
        #print(i.name)
        Drop_snap(i)


if __name__ == "__main__":
    main()
    print("DOing all.....")