import random

mac = [0x52, 0x54, 0x00,
       random.randint(0x00, 0x7f),
       random.randint(0x00, 0xff),
       random.randint(0x00, 0xff)]

def function1(x):
    return "%02x" % x

t = map(function1,mac)
p = ":".join(t)
print(type(p),p)

e = ["1","2","3","4","5"]

e1 = ("1","2","3","4","5")

e2 = {"chun":"13","aaa":"14","3":"16","4":"16","5":"16"}

b_dict = {'name':'chuhao','age':20,'province':'shanxi'}

print("".join(e1))

print ('{0},{1}'.format('chuhao', 20))

print ('{},{}'.format('chuhao', 20))

print ('{1},{0},{1}'.format('chuhao', 20))

a_list = ['chuhao',20,'china']
print ('my name is {chun},from {aaa},age is {aaa}'.format(**e2))
