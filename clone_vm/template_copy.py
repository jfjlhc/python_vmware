import pool_name as pooln
import vm_clone_view as jview
import vm_clone_si as jvm
from pyVmomi import vim
import vc_esxi_datas
pools = vc_esxi_datas.pool

copy_src_host = vc_esxi_datas.copy_src_host
copy_dest_host = vc_esxi_datas.copy_dest_host
dest_datastore = jview.get_host_datastore(copy_dest_host)
datacenters = jview.get_datacenter(copy_dest_host)
b = jview.get_path(datacenters)

def dest_host(vimtype, name):
    si,_ = jvm.get_vc_si()
    content = si.RetrieveServiceContent()
    objView = content.viewManager.CreateContainerView(content.rootFolder,
                                                      [vim.ComputeResource],
                                                      True)
    vmList = objView.view
    objView.Destroy()
    obj = None
    for i in vmList:
        if i.name == copy_dest_host:
            objView2 = content.viewManager.CreateContainerView(i,
                                                               [vimtype],

                                                               True)
            vmList2 = objView2.view

    for c in vmList2:
        if name:
            if c.name == name:
                obj = c
                break
        else:
            obj = None
            break
    return obj

def copy_template():
    si,_ = jvm.get_vc_si()
    content = si.RetrieveServiceContent()
    objView = content.viewManager.CreateContainerView(content.rootFolder,
                                                      [vim.ComputeResource],
                                                      True)
    vmList = objView.view
    objView.Destroy()

    for i in vmList:
        if i.name == copy_src_host:
            objView = content.viewManager.CreateContainerView(i,
                                                               [vim.VirtualMachine],

                                                               True)
            vmList = objView.view
            objView.Destroy()
            for vm in vmList:
                if vm.resourcePool is None:
                    if not dest_host(vim.ResourcePool, pools):
                        pooln.brower_data(pools, vc_esxi_datas.datacenters, vc_esxi_datas.copy_dest_host)
                    datastore = jview.get_object([vim.Datastore], dest_datastore)
                    resource_pool = jview.get_object([vim.ResourcePool], pools)

                    relospec = vim.vm.RelocateSpec()
                    relospec.datastore = datastore
                    relospec.pool = resource_pool

                    spec1 = vim.vm.CloneSpec()
                    spec1.location = relospec
                    spec1.powerOn = False
                    return (vm.Clone(folder=b, name=vm.name + "_j", spec=spec1))
