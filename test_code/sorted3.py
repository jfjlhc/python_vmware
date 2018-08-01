from operator import itemgetter, attrgetter

student_tuples = [
        ('john', 'Z', 15),
        ('jane', 'G', 12),
        ('dave', 'J', 12),
        ('apple', 'A', 100),
        ('cat', 'A', 99),
]


L = sorted(student_tuples, key=itemgetter(0,1))
print(L)

def numeric_compare(x,y):
    return x-y
l1 = sorted([5, 2, 4, 1, 3], cmp=numeric_compare)

print (l1)

"""cmp(x, y) -> -1, 0, 1 比较函数：x<y 返回-1，x=y返回0，x>y返回1。在py3.0中被移除了。
key 键函数：指定排序的对象"""












