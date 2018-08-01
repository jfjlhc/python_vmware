from pyVmomi import vim

import vm_clone_view as jview

type1 = vim.ComputeResource

type2 = vim.Datacenter

type2 = vim.Folder

type3 = vim.VirtualMachine

type4 = vim.ResourcePool

type5 = vim.Datastore

type6 = vim.StoragePod

type7 = vim.Network

copy_src_host = "192.168.1xxx4"

copy_dest_host = "192.168.xxx6"

dest_datastore = jview.get_host_datastore(copy_dest_host)##"datastore1"

datacenters = jview.get_datacenter(copy_dest_host)  ##"backup"

folder = jview.get_path(datacenters) ##"vim.Folder:group-v9547,vm"

host11 = jview.get_object([vim.ComputeResource],copy_dest_host)#" 19xxx6"

pools = host11.resourcePool.resourcePool[1].name

pools2 = host11.resourcePool.name

pool = "jfj_template"
