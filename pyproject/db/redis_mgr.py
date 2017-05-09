
#coding:gbk

from multiprocessing import Process,Queue,Pool
import multiprocessing
import os, time, random

# д���ݽ���ִ�еĴ���:
def write(q,lock):
    for value in ['A', 'B', 'C']:
        print 'Put %s to queue...' % value
        # with lock:
        q.put(value)

# �����ݽ���ִ�еĴ���:
def read(q):
    while True:
        if not q.empty():
            value = q.get(False)
            print 'Get %s from queue.' % value
            time.sleep(random.random())
        else:
            break

if __name__=='__main__':
    manager = multiprocessing.Manager()
    # �����̴���Queue�������������ӽ��̣�
    q = manager.Queue()
    lock = manager.Lock() #��ʼ��һ����
    p = Pool(processes=5)
    pw = p.apply_async(write,args=(q,lock))
    pr = p.apply_async(read,args=(q,))
    p.close()
    p.join()
