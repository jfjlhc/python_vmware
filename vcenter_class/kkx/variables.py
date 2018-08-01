#coding=utf-8
from pyVmomi import vim
"""passwd"""

class Variables(object):

    def __init__(self):

        self.vcenter = "192.168.134.231"
        self.vc_user = "jfj"
        self.vc_passwd = "pass2017!@#$"
        self.desc_host = "192.168.134.99"
        self.desc_pool = "jfjlxf"

        """默认路由和子网掩码"""
        self.vm_gateway = "192.168.140.1"
        self.vm_netmask = "255.255.255.0"

        self.vm_1th = "centosjfj"##特别注意不要有数据中心内虚拟机重名，否则obj的调用将随机选择
        self.vm_1th_ip = "192.168.134.119"
        self.vm_1th_gw = "192.168.134.65"
        self.vm_1th_vlan = {"1":"vlan126"}
        #
        #
        # self.vm_2th = "ubuntu14_server_DM_alarmpot_dockerhost_17.241"
        # self.vm_2th_ip = "192.168.117.24"
        # self.vm_2th_gw = "192.168.117.1"
        # self.vm_2th_vlan = {"1":"test121"}
        #
        # self.vm_3th = "centos69_server_DM_deploy_vmwareagent_17.28"
        # self.vm_3th_ip = "192.168.117.28"
        # self.vm_3th_gw = "192.168.117.1"
        # self.vm_3th_vlan = {"1":"test121"}
        #
        # self.vm_4th = "centos69_server_MS_data_process_17.22"
        # self.vm_4th_ip = "192.168.117.22"
        # self.vm_4th_gw = "192.168.117.1"
        # self.vm_4th_vlan = {"1":"test121"}
        #
        # self.vm_5th = "centos69_server_MS_userweb_svr_17.36"
        # self.vm_5th_ip = "192.168.117.36"
        # self.vm_5th_gw = "192.168.117.1"
        # self.vm_5th_vlan = {"1":"test121"}
        #
        # self.vm_6th = "centos69_server_SF_share_dir_svr_17.25"
        # self.vm_6th_ip = "192.168.117.25"
        # self.vm_6th_gw = "192.168.117.1"
        # self.vm_6th_vlan = {"1":"test121"}
        #
        # self.vm_7th = "double_ipmac1"
        # self.vm_7th_ip = "172.18.11.33"
        # self.vm_7th_gw = "172.18.11.250"
        # self.vm_7th_vlan = {"1":"test121"}
        #
        # self.vm_8th = "outside_real_host_outsvr_smsos_10.10.10.6_hj"
        # self.vm_8th_ip = "10.10.10.6"
        # self.vm_8th_gw = "10.10.10.254"
        # self.vm_8th_vlan = {"1":"test121"}
        #
        # self.vm_9th = "outside_fake_out_host_adminhost_10.10.10.22_hj"
        # self.vm_9th_ip = "10.10.10.22"
        # self.vm_9th_gw = "10.10.10.254"
        # self.vm_9th_vlan = {"1":"test121"}
        #
        # self.vm_10th = "outside_real_host_outsvr_app01_10.10.9.6_hj"
        # self.vm_10th_ip = "10.10.9.6"
        # self.vm_10th_gw = "10.10.9.254"
        # self.vm_10th_vlan = "vlan117_HyOs"
        #
        # self.vm_11th = "inside_real_host_oa_webman_172.18.10.12_hy11"
        # self.vm_11th_ip = "172.18.10.12"
        # self.vm_11th_gw = "172.18.10.254"
        # self.vm_11th_vlan = "vlan117_HyOs"
        #
        # self.vm_12th = "outside_fake_out_host_adminhost_10.10.10.22_hy"
        # self.vm_12th_ip = "10.10.10.22"
        # self.vm_12th_gw = "192.168.117.1"
        # self.vm_12th_vlan = "vlan117_HyOs"
        #
        # self.vm_13th = "outside_fake_out_host_app03_10.10.10.3_hy"
        # self.vm_13th_ip = "10.10.10.3"
        # self.vm_13th_gw = "192.168.117.1"
        # self.vm_13th_vlan = "vlan117_HyOs"
        #
        # self.vm_14th = "outside_real_host_outsvr_app01_10.10.9.6_hy"
        # self.vm_14th_ip = "10.10.9.6"
        # self.vm_14th_gw = "192.168.117.1"
        # self.vm_14th_vlan = "vlan117_HyOs"
        #
        # self.vm_15th = "outside_real_host_outsvr_smsapi_10.10.9.31_hy"
        # self.vm_15th_ip = "10.10.9.31"
        # self.vm_15th_gw = "192.168.117.1"
        # self.vm_15th_vlan = "vlan117_HyOs"
        #
        # self.vm_16th = "outside_real_host_outsvr_smsos_10.10.10.6_hy"
        # self.vm_16th_ip = "10.10.10.6"
        # self.vm_16th_gw = "192.168.117.1"
        # self.vm_16th_vlan = "vlan117_HyOs"



        self.vimpc = vim.ComputeResource

        self.vimcenter = vim.Datacenter

        self.vimfolder = vim.Folder

        self.vimvm = vim.VirtualMachine

        self.vimpool = vim.ResourcePool

        self.vimstore = vim.Datastore

        self.vimstorage = vim.StoragePod

        self.vimnet = vim.Network

        self.Datastore = vim.Datastore
