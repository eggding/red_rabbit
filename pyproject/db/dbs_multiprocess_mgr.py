# -*- coding:utf-8 -*-

import multiprocessing
import time
from multiprocessing import Process,Queue,Pool
import multiprocessing
import os, time, random
import ffext

cb_serial = 0
g_dictDbsSerial2Fun = {}

nChannelNum = 5
nProcessNum = 5

def JobConsume(queue_, lock_, retQueue, retLock):
    import conf as conf
    dictDbCfg = conf.dict_cfg["dbs"]
    conn = ffext.ffdb_create('mysql://{0}/{1}/{2}/{3}'.format(dictDbCfg["host"], dictDbCfg["user"], dictDbCfg["pwd"], dictDbCfg["db"]))
    dictChannel = {}

    while True:
        job = None
        lock_.acquire()
        if queue_.empty() is False:
            job = queue_.get()
        lock_.release()


def AddJob2Queue(szSrcScene, nCbID, nSession, funObj, param):
    """
    :param szSrcScene:
    :param nCbID:
    :param nSession:
    :param funObj:
    :param param:
    :return:
    """
    if isinstance(nSession, int):
        nQueueID = 0
    else:
        nQueueID = nSession % nProcessNum

manager = multiprocessing.Manager()
resultQueue = manager.Queue()
resultLock = manager.Lock()

listChannelQueue = {}
for i in xrange(0, nProcessNum):
    listChannelQueue[i] = [manager.Queue(), manager.Lock()]

p = multiprocessing.Pool(processes=nProcessNum)

for i in xrange(0, nProcessNum):
    pw = p.apply_async(JobConsume, args=(listChannelQueue, resultQueue, resultLock))

# p.join()
