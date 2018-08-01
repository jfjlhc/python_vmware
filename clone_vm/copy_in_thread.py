#coding=utf-8
#!/usr/bin/env python
import sys
import time
from pyVmomi import vim, vmodl
import pool_name as pooln
import vc_esxi_datas as datas
import vm_clone_si as jvm
import vm_clone_view as jview
from more_thread.hypot_threadpool import CThreadManager

sys.path.append("../vm_order")

"""当克隆虚拟机失败提示spec.location.host错误的时候，
多数是资源池或虚拟机在数据中心有重名"""


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
        if i.name == datas.copy_dest_host:
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

def fun1(args):
    vm11 = args['vm11']

    datastore11 = jview.get_object([vim.Datastore], datas.dest_datastore)
    resource_pool11 = pooln.get_host_pool(vim.ComputeResource, "Resources")

    relospec11 = vim.vm.RelocateSpec()
    relospec11.datastore = datastore11
    relospec11.pool = resource_pool11

    spec11 = vim.vm.CloneSpec()
    spec11.location = relospec11
    spec11.powerOn = False
    vm11.Clone(folder=datas.folder, name=vm11.name + "_j", spec=spec11)

def fun2(args):
    pool = args['pool']
    vm = args['vm']

    pools = pool.name + "_j"
    pooln.brower_data(pools, datas.datacenters, datas.copy_dest_host)

    datastore = jview.get_object([vim.Datastore], datas.dest_datastore)
    resource_pool = jview.get_object([vim.ResourcePool], pools)

    relospec = vim.vm.RelocateSpec()
    relospec.datastore = datastore
    relospec.pool = resource_pool

    spec1 = vim.vm.CloneSpec()
    spec1.location = relospec
    spec1.powerOn = False
    vm.Clone(folder=datas.folder, name=vm.name + "_j", spec=spec1)

def main():
    thread_manager = CThreadManager(max_work_count=100, max_thread_count=40,
                                    min_thread_count=20, add_change_count=10,
                                    min_free_count=1)
    thread_manager.setDaemon(True)
    thread_manager.start()

    si,_ = jvm.get_vc_si()
    content = si.RetrieveServiceContent()
    objView = content.viewManager.CreateContainerView(content.rootFolder,
                                                      [vim.ComputeResource],
                                                      True)
    vmList = objView.view
    objView.Destroy()

    for host in vmList:
        if host.name == datas.copy_src_host:
            objView = content.viewManager.CreateContainerView(host,
                                                              [vim.ResourcePool],
                                                              True)

            vmList = objView.view
            objView.Destroy()

            for pool in vmList:
                if pool.name == "Resources":
                    for vm11 in pool.vm:
                        thread_manager.add_work(fun1, {'vm11': vm11})
                elif not pool.name == "Resources":
                    if not dest_host(vim.ResourcePool, pool.name):
                        for vm in pool.vm:
                            thread_manager.add_work(fun2, {'vm': vm, 'pool': pool})

            time.sleep(4)

    while True:
        if not thread_manager.get_work_count():
            break
        time.sleep(1)


if __name__ == "__main__":
    main()