# coding=utf-8
from pyVmomi import vim
import sys, atexit
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
    host = "192.168.134.231"
    user = "jfj"
    password = "pass2017!@#$"
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
                                                      [vim.ComputeResource],
                                                      True)

    hostname = None
    for hostname in objView.view:
        if hostname.name == "192.168.134.107":
            objView = content.viewManager.CreateContainerView(hostname,
                                                              [vim.VirtualMachine],
                                                              True)
            vm = None
            for vm in objView.view:
                if vm.runtime.connectionState == "inaccessible":
                    vm.UnregisterVM()

                if vm.runtime.connectionState == "orphaned":
                    vm.UnregisterVM()
            objView.Destroy()


if __name__ == "__main__":
    main()
