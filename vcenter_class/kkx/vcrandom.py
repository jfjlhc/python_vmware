#coding = utf-8
#!/usr/bin/python

import random
import datetime
import hashlib
import requests
import sys
sys.path.append('../')


def rand_char_str(length):
    charStr = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    charStrList = list(charStr)
    random.shuffle(charStrList)
    randomStr = random.sample(charStrList, length)
    return ''.join(randomStr)

def get_rand_number():
    nowTime = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    randomNum = random.randint(10, 100000000000)
    randomNum = str(0) + str(randomNum)
    uniqueNum = str(nowTime) + str(randomNum)
    return uniqueNum

def get_md5(file_path):
    try :
        with open(file_path, 'rb') as f:
            m = hashlib.md5()
            while True:
                buff = f.read(4096)
                if not buff:
                    break
                m.update(buff)
            md5_hex = m.hexdigest()
    except Exception as e:
        return None
    return md5_hex


def rand_num(length):
    charStr = '0123456789'
    charStrList = list(charStr)
    random.shuffle(charStrList)
    randomStr = random.sample(charStrList, length)
    return ''.join(randomStr)

# if __name__ == "__main__":
#     print(rand_num(2))