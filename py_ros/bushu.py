#coding=utf-8
from librouteros import connect
"""修改ROS"""
api = connect(username='admin', password='pass1234!@#$', host='192.168.137.66',port=8728)

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

    array1 = {'action': 'dst-nat', 'chain': 'dstnat', 'dst-address': address, 'protocol': 'tcp','dst-port': '53353',  'to-addresses': '192.168.6.2','to-ports':'53353',}
    api(cmd='/ip/firewall/nat/add', **array1)

    array2 = {'action': 'dst-nat', 'chain': 'dstnat', 'dst-address': address, 'protocol': 'tcp',
              'to-addresses': '192.168.6.2', }
    api(cmd='/ip/firewall/nat/add', **array2)



if __name__ == "__main__":

    for nat in natt:
        print (nat)
        # for key in nat:
        #     print (nat[key])
        #     # if nat[key] == "192.168.6.2":
        #     #     dic1['.id'] = (nat['.id'])
        #     #     deladdress(dic1)






api.close()
