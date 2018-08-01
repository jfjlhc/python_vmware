#!/usr/bin/env python
import sys
sys.path.append("../clone_vm")
import vm_clone_view as jview
from pyVmomi import vim, vmodl
import vm_clone_si as jvm

b = jview.get_path("jfjjjj")

datastore =jview.get_object([vim.Datastore],'data121')
resource_pool = jview.get_object([vim.ResourcePool],'jfj_copy_tmp')

relospec = vim.vm.RelocateSpec()
relospec.datastore =datastore
relospec.pool = resource_pool

spec1 = vim.vm.CloneSpec()
spec1.location = relospec
spec1.powerOn = False

vm_list = ['inside_real_host_core_intdb_172.18.11.33',
'inside_real_host_insvr_adsvr_172.18.10.20',
'inside_real_host_insvr_adsvr_172.18.10.200',
'inside_real_host_insvr_adsvr_172.18.10.210',
'inside_real_host_insvr_appdev_172.18.10.201-172.18.11.201',
'inside_real_host_oa_webman_172.18.10.12',
'outside_fake_out_host_adminhost_10.10.10.22',
'outside_fake_out_host_app03_10.10.10.3',
'outside_real_host_outsvr_app01_10.10.9.6',
'outside_real_host_outsvr_nfsos_10.10.10.10-172.16.10.10',
'outside_real_host_outsvr_smsapi_10.10.9.31',
'outside_real_host_outsvr_smsos_10.10.10.6',
'outside_real_host_outsvr_www_10.10.9.5-172.16.9.5',
'centos69_server_DC_data_collect_117.20',
'centos69_server_DM_deploy_svr_117.21',
'centos69_server_MS_data_process_117.22',
'centos69_server_MS_userweb_svr_117.26',
'centos69_server_MS_userweb_svr_117.36',
'centos69_server_SF_share_dir_svr_117.25',
'ROS_192.168.134.100']



def main():
    si = None
    si,_ = jvm.get_vc_si()
    content = si.RetrieveServiceContent()
    objView = content.viewManager.CreateContainerView(content.rootFolder,
                                                      [vim.ComputeResource],
                                                      True)
    vmList = objView.view
    objView.Destroy()

    for host in vmList:
        if host.name == "192.168.134.115":
            objView = content.viewManager.CreateContainerView(host,
                                                               [vim.VirtualMachine],

                                                               True)
            vmList = objView.view
            objView.Destroy()
            for vm in vmList:
                if vm.name in vm_list:
                    vm.Clone(folder=b, name=vm.name + "_h", spec=spec1)

if __name__ == "__main__":
    main()
    print("DOing all.....")