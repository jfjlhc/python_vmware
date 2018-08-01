# -*- coding: utf-8 -*-
#!/usr/bin/python
from pyVmomi import vim
from pyVmomi import vmodl
import time
import requests
import os
import random
import subprocess
import logging
from datetime import timedelta, datetime
import sys
logging.captureWarnings(True)
sys.path.append("../")
# reload(sys)
# sys.setdefaultencoding('utf-8')

"""unicode()函数在Python 3里不再存在了
    Python 3只有一种字符串类型
"""

kel = unicode('中文string','utf-8')
print(type(kel))
print (kel.encode('utf-8'))
print(type(kel.encode('utf-8')))

print("-------------------------------------------------------")
s = u'中文string'
s1 = '中文string'
print(type(s))
print(type(s1))
print (type(s.encode('utf-8')))

lable = unicode('网络适配器 1','utf-8')
print(lable)
