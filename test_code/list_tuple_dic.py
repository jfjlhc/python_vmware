#coding=utf-8

def one():
    array = [{'vmhost_name': '[hy_ctf] - gateway_flow_layer_190.100__j',
                'vmhost_ip': '172.18.11.133',
                'vmhost_subnet': '255.255.255.0',
                'vmhost_gateway': '172.18.11.1', 'vmhost_mac': '00:50:56:81:05:d5',
                'new_vmhost_name': 'jfj_modify_ip'}]

    for dic in array:
        print(dic.get("vmhost_ip",''))
        dic2 = dic


def two():
    config = {}

    config["SERVER"] = "192.168.134.99"
    config["USERNAME"] = "root"
    config["PASSWORD"] = "JcatPass0197"


    print(config)

def three_one():
    def three():
        a = ('wolf', 'elephant', 'penguin')

        b = ['apple', 'mango', 'carrot', 'banana']

        c = {'Swaroop': 'swaroopch@byteofpython.info',
             'Larry': 'larry@wall.org',
             'Matsumoto': 'matz@ruby-lang.org',
             'Spammer': 'spammer@hotmail.com'
             }

        print(a, "\n", b, "\n", c)
        b.append("port")
        print("\n")
        print(b)
        print("\n")

def three():
    a = ('wolf', 'elephant', 'penguin')

    b = ['apple', 'mango', 'carrot', 'banana']

    c = {'Swaroop': 'swaroopch@byteofpython.info',
          'Larry': 'larry@wall.org',
          'Matsumoto': 'matz@ruby-lang.org',
          'Spammer': 'spammer@hotmail.com'
          }

    for i in a:
        print(i)
    for j in b:
         print(j)
    for h,k in c.items():
        print(h,k)

def four():
    d = [
        ('john', 'Z', 15),
        ('jane', 'G', 12),
        ('dave', 'J', 12),
        ('apple', 'A', 100),
        ('cat', 'A', 99),
    ]

    for i in d:
        print(i)
    print(d[1][1])

def five():
    e = [{'Swaroop': 'swaroopch@byteofpython.info',
          'Larry': 'larry@wall.org',
          'Matsumoto': 'matz@ruby-lang.org',
          'Spammer': 'spammer@hotmail.com'
          }]
    for h,k in e[0].items():
        print(h,k)

def six(**kwds):
    ip = kwds.get('new_name', '')

    print(ip)
    print(kwds)

if __name__ == "__main__":
    # vm_name = "aaa"
    # new_name = "vvv"
    # six(vm_name=vm_name, new_name=new_name)
    one()