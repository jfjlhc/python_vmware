# -*- coding: utf-8 -*-
import Queue
import threading 
import time

class CThreadManager(threading.Thread):
    '''
        max_work_count                最大任务数
        max_thread_count              最大线程数
        min_thread_count              最低线程数(初始化线程数)
        add_change_count              递变数
        min_free_count                最低空闲线程数
    '''
    def __init__(self, max_work_count = 100, max_thread_count = 40,
                 min_thread_count = 10, add_change_count = 10, min_free_count = 1):

        super(CThreadManager, self).__init__()
        self.max_work_count = max_work_count
        self.max_thread_count = max_thread_count
        self.min_thread_count = min_thread_count
        self.add_change_count = add_change_count
        self.min_free_count = min_free_count
        self.work_queue = Queue.Queue(self.max_work_count)
        self.threads = []
        self.__create_work_thread(self.min_thread_count)
        
    def __create_work_thread(self, thread_count):
        #剩余的总数
        counts = self.max_thread_count - len(self.threads)
        #剩余总数 - 需要增加的数 < 0
        if counts - thread_count < 0:
            thread_count = counts
            
        if thread_count == 0:
            return
        
        for i in range(thread_count):
            self.threads.append(CWorkThread(self.work_queue)) 
    
    def get_work_count(self):
        work_count = 0
        for thread in self.threads:
            if thread.is_working():
                work_count += 1
        return work_count
    
    def add_work(self, call_back, args):
        no_work_count = 0
        for thread in self.threads:
            if no_work_count > 1:
                break
            
            if not thread.is_working():
                no_work_count += 1
              
        #当空闲线程小于等于1个时，尝试再新建10个线程  
        if no_work_count <= 1:
            self.__create_work_thread(self.add_change_count)
            
        self.work_queue.put((call_back, args))
        
    def run(self):
        while True:
            no_work_count = 0
            need_free = False
            
            time.sleep(5)
            
            #当前线程数量大于最小线程数时再处理
            if len(self.threads) > self.min_thread_count:
                for thread in self.threads:
                    if not thread.is_working():
                        no_work_count += 1
                        #当空闲线程数大于当前线程数一半, 需要释放
                        if no_work_count > (len(self.threads) // 2):
                            need_free = True
                            break
                
                if need_free:
                    #如果释放了5个线程, 空闲线程大于最低空闲线程数, 可以释放
                    if no_work_count - 5 > self.min_free_count:
                        i = 0
                        for index in range(len(self.threads)):
                            if not self.threads[index].is_working() and i < 5:
                                self.threads[index].set_exit()
                                self.threads[index] = None
                                i += 1
                        self.threads = filter(lambda thread:thread != None, self.threads)

class CWorkThread(threading.Thread):
    def __init__(self, work_queue):
        super(CWorkThread, self).__init__()
        self.exit = False
        self.work_queue = work_queue
        self.is_work = False
        self.setDaemon(True)
        self.start() 
    
    def is_working(self):
        return self.is_work
    
    def set_exit(self):
        self.exit = True
        
    def run(self):
        while not self.exit:
            if not self.work_queue.empty():
                try:
                    call_back, args = self.work_queue.get()
                    self.is_work = True
                    call_back(args)
                    self.work_queue.task_done()
                    self.is_work = False
                except Exception as e:
                    break
            time.sleep(1)
                 
def call(**x):
    time.sleep(3)
    
if __name__ == '__main__':
    t = CThreadManager()
    t.setDaemon(True)
    t.start()     
    
    i = 0
    while i < 200:
        t.add_work(call, a = i)
        i += 1
        
    time.sleep(50)
    print ('start new add1')
    
    i = 0
    while i < 200:
        t.add_work(call, a = i)
        i += 1    

    time.sleep(50)
    print ('start new add2')
    
    i = 0
    while i < 200:
        t.add_work(call, a = i)
        i += 1    

    while True:
        time.sleep(1000)