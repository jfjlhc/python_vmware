#coding=utf-8
from pyVmomi import vim
import sys,atexit
import ssl
from pyVim.connect import SmartConnect, Disconnect

def set_vc_si(host, user, port, password, context):
    try:
        si1 = SmartConnect(host=host, user=user, pwd=password,
                           port=port, sslContext=context)
        if not si1:
            print("Can't connect to the host with given user and password")
            sys.exit()

        atexit.register(Disconnect, si1)


    except Exception as e:
        print("catch the exception: ", str(e))
    return si1


def get_vc_si():
    host = "192.168.139.167"
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




def main():
    si = get_vc_si()
    content = si.RetrieveServiceContent()
    objView = content.viewManager.CreateContainerView(content.rootFolder,
                                                      [vim.VirtualMachine],
                                                      True)
    vmList = objView.view
    objView.Destroy()

    for vm in vmList:
        vm.UnregisterVM()


if __name__ == "__main__":
    main()
    #print("所有虚拟机已经关闭了“)
