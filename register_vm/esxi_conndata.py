#coding=utf-8
import os
import ssl
import atexit
import sys
import Resister_Vmfs_main as jfj
from pyVim import connect
from pyVim.connect import SmartConnect, Disconnect
from pyVmomi import vim
"""edit by jifujun
自动化判断是否有存储，有几个，存储的状态，如果卸载状态就会挂载硬盘、如果没存储就会自动检测服务器有多少个阵列
然后添加阵列、批量添加虚拟机注册到清单、并且开启电源、应答虚拟机问题（如硬盘拆除过需要回答虚拟机是移动 还是克隆）、最后自动
批量添加模板到vcenter，如果产品没有vcenter则自动省去这步骤。
"""

esxi_host = jfj.esxi_host
esxi_user = jfj.esxi_user
esxi_passwd = jfj.esxi_passwd

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
        dic={}
        instance = get_vc_si()
        atexit.register(connect.Disconnect, instance)
        content = instance.RetrieveContent()
        container = content.viewManager.CreateContainerView(content.rootFolder, [vim.HostSystem], True)
        hostobj = container.view[0]

        container.Destroy()
        obj = hostobj.configManager.storageSystem.storageDeviceInfo
        i = 1
        for device in obj.scsiLun:
            if isinstance(device,vim.HostScsiDisk):
                dic[i]=device.canonicalName##"naa.614187705dd3e10021456a2d05616dc3"
                i+=1
        j=0
        for devname in dic.values():
            j+=1
            dp = "/vmfs/devices/disks/%s"%devname
            vmfs_ds_options = hostobj.configManager.datastoreSystem.QueryVmfsDatastoreCreateOptions(devicePath=dp,
                                                                                                    vmfsMajorVersion=5)

            vmfs_ds_options[0].spec.vmfs.volumeName = "datat109"+str(j)
            print("现在开始添加存储器：")
            hostobj.configManager.datastoreSystem.CreateVmfsDatastore(vmfs_ds_options[0].spec)

        os.system("python jfjregister.py")


    except Exception as e:
        os.system("python jfjregister.py")



