#coding=utf-8
def file_read1():
    f = open('/root/123', 'r')
    line = f.readline()#
    print(line[0])  # 1
    print(line[-1])  # \n 回车
    print(line[-1:3])
    print(len(line))
    f.close()


def file_read():
    f = open("/root/123")

    while True:
        line = f.readline()#每次读一行！！
        if len(line) == 0:
            break
        print (line,)
    f.close()

def file_write():
    s = 'hello'.encode()
    s1 = b'hello'
    f = open("/root/123","rb+")#python3:rb+
    f.readline()
    f.seek(-1, 2)
    f.write(s)
    f.close()
    f = open("/root/123")
    while True:
        line = f.readline()
        if not line:
            break
        print (line,"\n")
    print(type(s1))

def file_write1():
    f = open("/root/123",'w')
    f.write("1237777777\n456\n789\n")
    f.close()
    f = open("/root/123")

    while True:
        line = f.readline()
        if len(line) == 0:
            break
        print (line )

def file_read3():


    # 打开文件
    fo = open("/root/runoob.txt", "rw+")

    print ("文件名为: ", fo.name)

    line = fo.readline()
    print ("读取的数据为: %s" % (line))

    # 重新设置文件读取指针到开头
    fo.seek(-1, 2)
    line = fo.readline()
    print ("读取的数据为: %s" % (line))

    # 关闭文件
    fo.close()

if __name__ == "__main__":
    file_write()
    #file_read1()
    #file_read3()
