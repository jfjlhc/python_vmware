import time

from more_thread.hypot_threadpool import CThreadManager

g_thread_manager = CThreadManager(max_work_count = 100, max_thread_count = 40, min_thread_count = 10, add_change_count = 10, min_free_count = 1)
g_thread_manager.setDaemon(True)
g_thread_manager.start()

def fun(args):
    print args
    time.sleep(5)
        
if __name__ == '__main__':
    args = dict(
        a = 1,
        b = 2,
        c = 3
    )
    
    g_thread_manager.add_work(fun, args)
    
    time.sleep(5)
    
    while True:
        if not g_thread_manager.get_work_count():
            break
        time.sleep(1)