#coding=utf-8
import pool_name as pooln
import vm_clone_view as jview
import vm_clone_si as jvm
from pyVmomi import vim
import template_copy as template
import vc_esxi_datas as datas
import Traversal_resourse as traver
import sys
sys.path.append("../")
from vm_order.vm_order import enable_auto_restart
from task.vcenter_task import WaitForTasks

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

def main():
    si,_ = jvm.get_vc_si()
    content = si.RetrieveServiceContent()
    objView = content.viewManager.CreateContainerView(content.rootFolder,
                                                      [vim.ComputeResource],
                                                      True)
    vmList = objView.view
    objView.Destroy()

    for host in vmList:
        if host.name == datas.copy_src_host:

            datastore11 = jview.get_object([vim.Datastore], datas.dest_datastore)
            resource_pool11 = pooln.get_host_pool(datas.type1, "Resources")

            relospec11 = vim.vm.RelocateSpec()
            relospec11.datastore = datastore11
            relospec11.pool = resource_pool11

            spec11 = vim.vm.CloneSpec()
            spec11.location = relospec11
            spec11.powerOn = False

            for vm11 in host.resourcePool.vm:
                vm11.Clone(folder=datas.folder, name=vm11.name + "_", spec=spec11)

            for pool in host.resourcePool.resourcePool:

                if not dest_host(vim.ResourcePool,pool.name):
                    pools = pool.name+"_"
                    pooln.brower_data(pools,datas.datacenters,datas.copy_dest_host)

                    datastore = jview.get_object([vim.Datastore], datas.dest_datastore)
                    resource_pool = jview.get_object([vim.ResourcePool], pools)

                    relospec = vim.vm.RelocateSpec()
                    relospec.datastore = datastore
                    relospec.pool = resource_pool

                    spec1 = vim.vm.CloneSpec()
                    spec1.location = relospec
                    spec1.powerOn = False
                    for vm in pool.vm:
                        vm.Clone(folder=datas.folder, name=vm.name + "_", spec=spec1)


                for pool2 in pool.resourcePool:

                    if not dest_host(vim.ResourcePool,pool2.name):
                        pools2 = pool2.name + "_"
                        pooln.second_data(pools,pools2,datas.datacenters,datas.copy_dest_host)

                        datastore = jview.get_object([vim.Datastore], datas.dest_datastore)
                        resource_pool = jview.get_object([vim.ResourcePool], pools2)

                        relospec = vim.vm.RelocateSpec()
                        relospec.datastore = datastore
                        relospec.pool = resource_pool

                        spec1 = vim.vm.CloneSpec()
                        spec1.location = relospec
                        spec1.powerOn = False

                        tasks = [vm.Clone(folder=datas.folder, name=vm.name + "_j", spec=spec1)
                                 for vm in pool2.vm]

                WaitForTasks(tasks, si)
                print("Now,clone vm is be done!")
                tasks = [template.copy_template()]
                WaitForTasks(tasks, si)
                print("Now,The template is copy in dest_host!")
                """接下来转换成模板"""
                traver.conver_template()
                print("traver is good over!")
                traver.delete_temp_pool()
                print("delete template pool is OK!,run over!")
                enable_auto_restart(si, datas.copy_dest_host)
                print("自动启动顺序设置完毕")

if __name__ == "__main__":
    main()