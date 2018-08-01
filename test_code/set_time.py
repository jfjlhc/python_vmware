import time,datetime
class Times(object):
    def __init__(self,hour,minute,second):
        self.hour = hour
        self.minute = minute
        self.second = second

    def __str__(self):

        return '%.2d:%.2d:%.3d' % (self.hour, self.minute, self.second)

t = Times(9,45,30)

print(t)
print(datetime.datetime.now().strftime("%Y%m%d%H%M%S"))