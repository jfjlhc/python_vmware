# encoding: UTF-8
import re

# 将正则表达式编译成s对象
s = re.compile("world aaa")

# 使用s匹配文本，获得匹配结果，无法匹配时将返回None
match = s.match('world aaaaaaaa')

if match:
    # 使用Match获得分组信息
    print (match.group())



