#!/usr/bin/python
from pyVmomi import vim
import vc_si as jvm


def get_path(datatcenter_name):  ##through the datacenter's folder
    si,_ = jvm.get_vc_si()
    content = si.RetrieveServiceContent()
    for datacenter1 in content.rootFolder.childEntity:
        if datacenter1.name == datatcenter_name:
            return datacenter1.vmFolder


def get_folder(datatcenter_name):  ##through the name find the path
    si = jvm.get_vc_si()
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
    si,_ = jvm.get_vc_si()
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
    si,_ = jvm.get_vc_si()
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
    si,_ = jvm.get_vc_si()
    content = si.content
    object = content.viewManager.CreateContainerView(content.rootFolder,
                                                     [vim.ComputeResource],
                                                     True)

    for host in object.view:
        if host.name == hosts:
            datatcenters = host.parent.parent.name
            break
    return datatcenters


