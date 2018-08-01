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
    host = "192.168.137.66"
    user = "root"
    password = "pass1234!@#$"
    port = 8081
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
                                                      [vim.Datacenter],
                                                      True)
    vmList = objView.view
    objView.Destroy()

    hostspec = vim.host.ConnectSpec()
    hostspec.hostName = "1.1.1.159"
    hostspec.userName = "root"
    hostspec.password = "pass1234!@#$"
    hostspec.port = 443
    hostspec.sslThumbprint = "8F:FE:FA:ED:B3:7C:84:A0:FB:0F:13:B1:94:FE:6E:50:DD:6B:A5:11"

    for i in vmList:
        if i.name == "esxi":
            i.hostFolder.AddStandaloneHost_Task(spec=hostspec,addConnected=True)



if __name__ == "__main__":
    main()
    print("DOing all.....")