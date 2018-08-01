from pyVmomi import vim
import vm_clone_si as jvm
import vc_esxi_datas as datas
cpuspec = vim.ResourceAllocationInfo()
cpuspec.expandableReservation = True
cpuspec.limit = -1
cpuspec.reservation = 0
cpuspec.shares = vim.SharesInfo(level="normal")

memoryspec = vim.ResourceAllocationInfo()
memoryspec.expandableReservation = True
memoryspec.limit = -1
memoryspec.reservation = 0
memoryspec.shares = vim.SharesInfo(level="normal")

poolspec = vim.ResourceConfigSpec()
poolspec.cpuAllocation = cpuspec
poolspec.memoryAllocation = memoryspec

def brower_data(names,datacenter_name,dest_host):
    try:
        si,_ = jvm.get_vc_si()
        content = si.content
        object = content.viewManager.CreateContainerView(content.rootFolder,
                                                          [vim.Datacenter],
                                                          True)
        vmList = object.view
        object.Destroy()
        for datacent in vmList:
            if datacent.name == datacenter_name:
                object2 = content.viewManager.CreateContainerView(content.rootFolder,
                                                                 [vim.ComputeResource],
                                                                 True)
                vmList2 = object2.view
                object2.Destroy()
                for host1 in vmList2:
                    if host1.name == dest_host:
                        pools = host1.resourcePool
                        pools.CreateResourcePool(name=names, spec=poolspec)

    except vim.fault.DuplicateName:
        print("The wrong")

def second_data(pool_name,names,datacenter_name,dest_host):
    try:
        si,_ = jvm.get_vc_si()
        content = si.content
        object = content.viewManager.CreateContainerView(content.rootFolder,
                                                         [vim.Datacenter],
                                                         True)
        vmList = object.view
        object.Destroy()
        for datacent in vmList:
            if datacent.name == datacenter_name:
                object2 = content.viewManager.CreateContainerView(content.rootFolder,
                                                                  [vim.ComputeResource],
                                                                  True)
                vmList2 = object2.view
                object2.Destroy()
                for host1 in vmList2:
                    if host1.name == dest_host:
                        pools0 = host1.resourcePool
                        for pool1 in pools0.resourcePool:
                            if pool1.name == pool_name:
                                pool1.CreateResourcePool(name=names, spec=poolspec)

    except vim.fault.DuplicateName:
        print("The wrong")

def get_object(vimtype, name):
    si = jvm.get_vc_si()
    content = si.content
    obj = None
    object = content.viewManager.CreateContainerView(content.rootFolder,
                                                     [vimtype],
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


def get_host_pool(vimtype, name):
    si,_ = jvm.get_vc_si()
    content = si.content
    obj = None
    object = content.viewManager.CreateContainerView(content.rootFolder,
                                                     [vimtype],
                                                     True)
    viewList = object.view
    object.Destroy()

    for host in viewList:
        if host.name == datas.copy_dest_host:
            object2 = content.viewManager.CreateContainerView(host,
                                                              [vim.ResourcePool],
                                                              True)
            viewList2 = object2.view
            object2.Destroy()

            for c in viewList2:
                if name:
                    if c.name == name:
                        obj = c
                        break
                else:
                    obj = None
                    break
            return obj
