#coding=utf-8
from librouteros import connect
"""修改ROS"""
api = connect(username='admin', password='gcse612589', host='192.168.88.2',port=28728)

ip = api(cmd='/ip/firewall/mangle/print')
natt = api(cmd='/ip/firewall/nat/print')

dic={}
dic1={}

def delnat(dic):
    # api.run('/ip/firewall/nat/remove',{'ID':dic})
    # print (dic)
    # print ()
    api(cmd='/ip/firewall/mangle/remove',**dic)

def deladdress(part):
    api(cmd='/ip/firewall/nat/remove', **part)



def read():
    global address
    ct = api(cmd='/ip/address/print')
    for ag in ct:
        for key in ag:
            if ag[key] == "ct4":
                address = ag['address']
                break

def run(part):
    try:
        api(cmd='/system/script/run', **part)
    except Exception as e:
        pass


def addnat():
    jfj = '!' + address

    array1 = {'action': 'dst-nat', 'chain': 'dstnat', 'dst-address': address, 'to-addresses': '192.168.10.100'}
    api(cmd='/ip/firewall/nat/add', **array1)

    array1 = {'action': 'dst-nat', 'chain': 'dstnat', 'dst-address': address, 'protocol': 'tcp','dst-port': '53322',  'to-addresses': '192.168.10.100','to-ports':'22',}
    api(cmd='/ip/firewall/nat/add', **array1)

    array2 = {'action': 'mark-routing', 'src-address': '192.168.129.2-192.168.129.190', 'dst-address': jfj,
              'new-routing-mark': 'VLAN129', 'chain': 'prerouting'}
    api(cmd='/ip/firewall/mangle/add', **array2)

    array3 = {'action': 'mark-routing', 'src-address': '192.168.126.2-192.168.126.190', 'dst-address': jfj,
              'new-routing-mark': 'VLAN126', 'chain': 'prerouting'}
    api(cmd='/ip/firewall/mangle/add', **array3)

    array4 = {'action': 'mark-routing', 'src-address': '192.168.127.2-192.168.127.190', 'dst-address': jfj,
              'new-routing-mark': 'VLAN127', 'chain': 'prerouting'}
    api(cmd='/ip/firewall/mangle/add', **array4)

    array5 = {'action': 'mark-routing', 'src-address': '192.168.128.2-192.168.128.190', 'dst-address': jfj,
              'new-routing-mark': 'VLAN128', 'chain': 'prerouting'}
    api(cmd='/ip/firewall/mangle/add', **array5)

    array6 = {'action': 'mark-routing', 'src-address': '192.168.132.2-192.168.132.190', 'dst-address': jfj,
              'new-routing-mark': 'VLAN132', 'chain': 'prerouting'}
    api(cmd='/ip/firewall/mangle/add', **array6)

    array7 = {'action': 'mark-routing', 'src-address': '192.168.125.2-192.168.125.190', 'dst-address': jfj,
              'new-routing-mark': 'VLAN125', 'chain': 'prerouting'}
    api(cmd='/ip/firewall/mangle/add', **array7)

    array8 = {'action': 'mark-routing', 'src-address': '192.168.50.2-192.168.50.190', 'dst-address': jfj,
              'new-routing-mark': 'VLAN50', 'chain': 'prerouting'}
    api(cmd='/ip/firewall/mangle/add', **array8)

    array9 = {'action': 'mark-routing', 'src-address': '192.168.150.2-192.168.150.190', 'dst-address': jfj,
              'new-routing-mark': 'VLAN150', 'chain': 'prerouting'}
    api(cmd='/ip/firewall/mangle/add', **array9)

    arrayA = {'action': 'mark-routing', 'src-address': '192.168.140.125-192.168.140.190', 'dst-address': jfj,
              'new-routing-mark': 'VLAN140', 'chain': 'prerouting'}
    api(cmd='/ip/firewall/mangle/add', **arrayA)

    arrayB = {'action': 'mark-routing', 'src-address': '192.168.100.0/24', 'new-routing-mark': 'wifi(vlan100)',
              'chain': 'prerouting'}
    api(cmd='/ip/firewall/mangle/add', **arrayB)

    arrayC = {'action': 'mark-routing', 'src-address': '192.168.134.0/24', 'new-routing-mark': 'VLAN134',
              'chain': 'prerouting'}
    api(cmd='/ip/firewall/mangle/add', **arrayC)

    arrayD = {'action': 'mark-routing', 'src-address': '192.168.45.2-192.168.45.190', 'new-routing-mark': 'VLAN45',
              'chain': 'prerouting'}
    api(cmd='/ip/firewall/mangle/add', **arrayD)

if __name__ == "__main__":
    if 1:
        read()

    part={"number":"script1"}
    run(part)
    part = {"number": "script3"}
    run(part)

    for ag in ip:
        for key in ag:
            if ag[key] == "prerouting":
                dic['.id']=(ag['.id'])
                delnat(dic)

    for nat in natt:
        for key in nat:
            if nat[key] == "192.168.10.100":
                dic1['.id'] = (nat['.id'])
                deladdress(dic1)

    for nat in natt:
        for key in nat:
            if nat[key] == "192.168.116.16":
                dic1['.id'] = (nat['.id'])
                deladdress(dic1)

    addnat()



api.close()
