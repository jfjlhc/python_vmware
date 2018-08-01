import random

a = random.randint(0x00, 0x7f)
b = random.randint(0x00, 0xff)
c = random.randint(0x00, 0xff)
d = 0xaf
print(a,"\n",b,"\n",c,"\n",d)

mac = [0x52, 0x54, 0x00,
       random.randint(0x00, 0x7f),
       random.randint(0x00, 0xff),
       random.randint(0x00, 0xff)]

print(mac)


# def function1(x, y):
#     return x + y

#
# z = map(lambda x,y:x+y, [1, 3, 5, 7, 9], [2, 4, 6, 8, 10])
# for i in z:
#     print(i)
# print(z)
# def function1(x):
#     return "%02x" % x
t = map(lambda x:"%02x" % x,mac)#此时的mac不是list了
p = ":".join(t)
print(p)


