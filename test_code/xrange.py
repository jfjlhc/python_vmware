
#!/usr/bin/python
# compare for multi threads
import time


def worker():
    print("worker")
    time.sleep(1)
    #return

a = [11,2,3,4,5]
if __name__ == "__main__":


    for i in list(xrange(5)):
        worker()
        print(i)
    print(list(xrange(5)))

    for i in xrange(5):
        worker()
        print(i)
    print(list(xrange(5)))