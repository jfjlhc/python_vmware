#!/usr/bin/env python
si = 11
obj = 12

def summ1(si,obj):
    return si+obj

dic = {
    'numCPUs': "aaaa",
    'numCoresPerSocket': "bbbb",
    'vm_name':summ1

}


arg = {
    'numCPUs': "aaaa",
    'vm_mac': 'vm_name',

}


print(arg['vm_mac'])
print(dic[arg['vm_mac']])
print(dic['vm_name'])
print(dic[arg['vm_mac']](si,obj))

dic2 = {'ret' : False, 'desc' : "aaa"}
print(len(dic2))


arg = {'alloc_type': 'network_configure', 'ip': '172.18.11.133',
       'gateway': '172.18.11.1', 'subnet': '255.255.255.0'}


def network(num,**kwds):
    key = num
    ip = kwds.get("ip")
    print(ip)

network(si,**arg)


