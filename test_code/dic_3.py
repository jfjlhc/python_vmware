config = {}

config["SERVER"] = "192.168.134.99"
config["USERNAME"] = "root"
config["PASSWORD"] = "JcatPass0197"


def to_config_string():
    s = ["#" * 19,
         "Testbed Configuration:",
         "*" * 19]
    s1 = s + ["   {}: {}".format(m, config[m])
          for m in sorted(config.keys())]
    s2 = s1 + ["=" * 200]
    print("\n".join(s2))

# if __name__ == "__main__":
#     to_config_string()
g_vms = {'vcenter-88-150': 1,
         'ros_192.168.134.67': 2,
         'centos69_server_SF_share_dir_svr_17.25': 3,
         'centos69_server_MS_userweb_svr_17.36': 4,
         'centos69_server_MS_userweb_svr_17.26': 5,
         'centos69_server_DC_data_collect_17.20': 6,
         'centos69_server_MS_data_process_17.22': 7,
         'centos69_server_DM_deploy_svr_17.21': 8,
         'centos69_server_DM_deploy_vmwareagent_17.28': 9,
         'ubuntu14_server_DM_alarmpot_dockerhost_17.24': 10}

print(type(g_vms.items()))##dict_items
print(g_vms.items())
a = sorted(g_vms.items(),key=lambda x:x[1],reverse=True)#数组，数组里面是元组
print(a)
# for j in a:
#     print(j)##元祖
# # for i in a:
# #     print(i[0])
# #     print(i[1])
# b = g_vms.keys()##dict_keys,数组，数组里面是字符串
# print(b)
# # for i in b:#数组
# #     print(i)
#
# c = g_vms.values()##dict_values,数组，数组里面是键值
# print(c)
# if 'vcenter-88-150' in g_vms:
#     print("aaa")
#
#
# for i in g_vms:
#     print(i)

# a = {'1': 'test121', 'vlan1': 'vlan117_HyOs'}
# print(a['1'])