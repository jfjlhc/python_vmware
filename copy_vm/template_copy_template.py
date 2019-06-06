from pyVmomi import vim
import sys,ssl

"""模板克隆成模板"""

def create_vcenter_si():
    vcenter_ip = '192.168.134.231'
    vcenter_user = 'jfj'
    vcenter_pwd = 'pass2017!@#$'
    vcenter_port = 443
    si = None

    import ssl
    from pyVim import connect
    import atexit
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE

    try:
        si = connect.SmartConnect(host=vcenter_ip, user=vcenter_user, pwd=vcenter_pwd,
                                  port=vcenter_port, sslContext=ssl_context)
        atexit.register(connect.Disconnect, si)
    except Exception as e:
        print(str(e))
    return si

def get_path(datatcenter_name):  ##through the datacenter's folder
    si = create_vcenter_si()
    content = si.RetrieveServiceContent()
    for datacenter1 in content.rootFolder.childEntity:
        if datacenter1.name == datatcenter_name:
            return datacenter1.vmFolder

def get_folder(datatcenter_name):  ##through the name find the path
    si = create_vcenter_si()
    content = si.content
    obj = None
    object = content.viewManager.CreateContainerView(content.rootFolder,
                                                     [vim.Datacenter],
                                                     True)
    for dcenter in object.view:
        if dcenter.name == datatcenter_name:
            object2 = content.viewManager.CreateContainerView(dcenter,
                                                              [vim.Folder],
                                                              True)
            for c in object2.view:
                # print(c)
                if True:
                    if c.name == "vm":
                        obj = c
                        break
                else:
                    obj = c
            return obj


def get_object(vimtype, name):
    si = create_vcenter_si()
    content = si.content
    obj = None
    object = content.viewManager.CreateContainerView(content.rootFolder,
                                                     vimtype,
                                                     True)
    viewList = object.view

    for c in viewList:
        if name:
            if c.name == name:
                obj = c
                break
        else:
            obj = None
            break
    return obj


def get_host_datastore(hosts):
    si = create_vcenter_si()
    content = si.content
    object = content.viewManager.CreateContainerView(content.rootFolder,
                                                     [vim.ComputeResource],
                                                     True)
    for host in object.view:
        if host.name == hosts:
            datastore=host.datastore[0].name
            break
    return datastore


def get_datacenter(hosts):
    si = create_vcenter_si()
    content = si.content
    object = content.viewManager.CreateContainerView(content.rootFolder,
                                                     [vim.ComputeResource],
                                                     True)

    for host in object.view:
        if host.name == hosts:
            datatcenters = host.parent.parent.name
            break
    return datatcenters

b = get_path("jfjjjj")

datastore = get_object([vim.Datastore],'data99_1')
resource_pool = get_object([vim.ResourcePool],'jfj_server')

relospec = vim.vm.RelocateSpec()
relospec.datastore =datastore
relospec.pool = resource_pool

spec1 = vim.vm.CloneSpec()
spec1.location = relospec
spec1.powerOn = False
spec1.template = True  //template

vm_list = ["win7_1"]

def main():
    si = create_vcenter_si()
    content = si.RetrieveServiceContent()
    objView = content.viewManager.CreateContainerView(content.rootFolder,
                                                      [vim.VirtualMachine],
                                                      True)
    vmList = objView.view
    objView.Destroy()

    for vm in vmList:
        if vm.resourcePool is None:
            if vm.name in vm_list:
                vm.Clone(folder=b, name=vm.name + "_j", spec=spec1)



if __name__ == "__main__":
    main()
    print("DOing all.....")