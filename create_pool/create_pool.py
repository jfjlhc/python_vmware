#!/usr/bin/env python
import sys
sys.path.append("../clone_vm")
from pyVmomi import vim
import vm_clone_si as jvm

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

def brower_data():
    try:
        si = None
        si = jvm.get_vc_si()
        content = si.content
        datacent = content.rootFolder.childEntity[2]
        # print(datacent)
        name = "Resources"
        pools = datacent.hostFolder.childEntity[5].resourcePool
        pools.CreateResourcePool(name=name, spec=poolspec)
    except vim.fault.DuplicateName:
        print("The wrong")

