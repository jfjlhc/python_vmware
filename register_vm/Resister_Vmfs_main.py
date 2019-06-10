#coding=utf-8
import os
import ssl
import atexit
import sys,time
from pyVim import connect
from pyVim.connect import SmartConnect, Disconnect
from pyVmomi import vim
"""write by jifujun tt"""

esxi_host = "192.168.137.144"
esxi_user = "root"
esxi_passwd = "Jeeseen.com.run1225!@#$"

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
    host = esxi_host
    user = esxi_user
    password = esxi_passwd
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


if __name__ == "__main__":
    try:
        instance = get_vc_si()
        atexit.register(connect.Disconnect, instance)
        content = instance.RetrieveContent()
        container = content.viewManager.CreateContainerView(content.rootFolder, [vim.HostSystem], True)
        hostobj = container.view[0]
        container.Destroy()


        for uuid in hostobj.datastore:
            if uuid.summary.accessible == False:
                dp = uuid.info.vmfs.uuid
                print("现在开始挂载存储：")
                hostobj.configManager.storageSystem.MountVmfsVolume(vmfsUuid=dp)

        print("请等待5S", time.sleep(5))
        os.system("python esxi_conndata.py")
    except Exception as e:
        os.system("python esxi_conndata.py")



