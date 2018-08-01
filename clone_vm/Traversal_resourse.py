import vm_clone_si as jvm
import vc_esxi_datas as datas

def delete_temp_pool():
    si,_ = jvm.get_vc_si()
    content = si.RetrieveServiceContent()
    object = content.viewManager.CreateContainerView(content.rootFolder,
                                                      [datas.type1],#host
                                                      True)
    vmList = object.view
    object.Destroy()
    for host in vmList:
        if host.name == datas.copy_dest_host:
            object2 = content.viewManager.CreateContainerView(host,
                                                              [datas.type4],#pool
                                                              True)
            vmList2 = object2.view
            object2.Destroy()
            for pool in vmList2:
                if pool.name == datas.pool:
                    pool.Destroy()


def conver_template():
    si,_ = jvm.get_vc_si()
    content = si.RetrieveServiceContent()
    object = content.viewManager.CreateContainerView(content.rootFolder,
                                                     [datas.type1],#host
                                                     True)
    vmList = object.view
    object.Destroy()
    for host in vmList:
        if host.name == datas.copy_dest_host:
            object = content.viewManager.CreateContainerView(host,
                                                              [datas.type4],#pool
                                                              True)
            vmList = object.view
            object.Destroy()
            for pool in vmList:
                if pool.name == datas.pool:
                    object = content.viewManager.CreateContainerView(pool,
                                                                      [datas.type3],#vmguest
                                                                      True)
                    vmList = object.view
                    object.Destroy()
                    for vm in vmList:
                        vm.MarkAsTemplate()
