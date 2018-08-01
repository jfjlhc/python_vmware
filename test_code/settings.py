"""
Network, VMware, and general settings for deploying a new Linux VM
"""

from netaddr import IPNetwork, IPAddress

"""
General settings
"""
deploy_settings = dict()
deploy_settings["dns_servers"]      = ['8.8.8.8','8.8.4.4']
deploy_settings["vserver"]          = "vcenter.example.com"
deploy_settings["port"]             = 443
deploy_settings["username"]         = "admin"
deploy_settings["password"]         = "password"
deploy_settings["mailfrom"]         = 'root@example.com'

"""
Networks
"""
# define settings for each of our networks
net = dict()

internal_omaha = IPNetwork("192.168.134.0/24")
net[internal_omaha] = dict()
net[internal_omaha]["datacenter_name"] = 'Omaha'
net[internal_omaha]["cluster_name"]    = 'Omaha Server Cluster'
net[internal_omaha]["datastore_name"]  = 'Omaha datastore'
net[internal_omaha]["network_name"]    = 'Omaha Internal 1'
net[internal_omaha]["gateway"]         = '172.9.9.1'
net[internal_omaha]["subnet_mask"]     = str(internal_omaha.netmask)

routable_omaha = IPNetwork("192.168.134.0/24")
net[routable_omaha] = dict()
net[routable_omaha]["datacenter_name"] = 'Omaha'
net[routable_omaha]["cluster_name"]    = 'Omaha Server Cluster'
net[routable_omaha]["datastore_name"]  = 'Omaha datastore'
net[routable_omaha]["network_name"]    = 'Omaha Routable 1'
net[routable_omaha]["gateway"]         = '123.456.78.91'
net[routable_omaha]["subnet_mask"]     = str(routable_omaha.netmask)

'''
# Storage networks
# '''
internal_storage = IPNetwork("192.168.134.0/24")
net[internal_storage] = dict()
net[internal_storage]["network_name"] = '192.168.134x storage net'
net[internal_storage]["subnet_mask"]  = str(internal_storage.netmask)