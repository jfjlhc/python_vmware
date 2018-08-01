names = locals()
for i in range(1, 10):
    i = names['x%s' % i]
    print (i)
    break
"""动态变量名称"""