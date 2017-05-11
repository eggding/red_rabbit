
#coding:gbk

from multiprocessing import Process,Queue,Pool
import multiprocessing
import os, time, random

# 写数据进程执行的代码:
def write(q):
    while True:
        for value in ['A', 'B', 'C']:
            print 'Put %s to queue...' % value
            # with lock:
            q.put(value)

# 读数据进程执行的代码:
def read(q):
    while True:
        if not q.empty():
            value = q.get(False)
            print 'Get %s from queue.' % value
            time.sleep(random.random())
        else:
            break

if __name__=='__main__':
    q = Queue()
    p = Process(target=read, args=(q,))
    p.start()
    while True:
        write(q)