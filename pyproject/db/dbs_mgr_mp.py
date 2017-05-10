# -*- coding: utf-8 -*-
# @Author  : jh.feng

import random, time
import json
import ffext
import rpc.rpc_def as rpc_def
import dbs_def as dbs_def
import MySQLdb
import multiprocessing as multiprocessing
import util.tick_mgr as tick_mgr
import conf as conf

class SyncJob(object):
    def __init__(self):
        self.m_funObj = None
        self.m_funParam = None
        self.m_nQueueID = None
        self.m_nSession = None
        self.m_szSrcScene = None
        self.m_cb = None

    def Init(self, funObj, nQueueID, nSession, szSrcScene, cb_id=0, funParam=None):
        self.m_funObj = funObj
        self.m_funParam = funParam
        self.m_nQueueID = nQueueID
        self.m_nSession = nSession
        self.m_szSrcScene = szSrcScene
        self.m_cb = cb_id

    def SetSession(self, session):
        self.m_nSession = session

    def GetQueueID(self):
        return self.m_nQueueID

    def GetSceneName(self):
        return self.m_szSrcScene

    def GetCbID(self):
        return self.m_cb

    def GetSession(self):
        return self.m_nSession

    def GetParam(self):
        return self.m_funParam

    def exe(self, dbsConn):
        return self.m_funObj(dbsConn, self)

class DbsMgr(object):
    def __init__(self):
        self.m_nQueueNum = conf.dict_cfg["dbs"]["queue_num"]
        self.m_dictChannel2Queue = {}
        self.m_dictChannel2QueueRet = {}
        self.m_nTick2CheckWorkQueue = 1
        self.m_nConn = None
        self.m_bInited = False

        self.m_nProcessedJobNum = 0

        self.m_queueWork = None
        self.m_queueWorkRet = None

        self.Init()

    def DispathWorkRet(self):
        tick_mgr.RegisterOnceTick(self.m_nTick2CheckWorkQueue, self.DispathWorkRet)
        nQueueRandom = 0 # random.randint(0, self.m_nQueueNum - 1)
        queueRet = self.m_dictChannel2QueueRet[0]
        c = 0
        while queueRet.empty() is False:
            szScene, szSerial = self.m_dictChannel2QueueRet[nQueueRandom].get()
            ffext.call_service(szScene, rpc_def.OnDbAsynCallReturn, json.dumps(szSerial))

            self.m_nProcessedJobNum += 1
            c += 1
            if c > 50:
                break
            print("dbs self.m_nProcessedJobNum ", self.m_nProcessedJobNum, self.m_dictChannel2QueueRet[nQueueRandom].qsize())

    def worker(self, nQueueID, workQueue, retQueue):
        cfg = conf.dict_cfg["dbs"]
        szHost, port = cfg["host"].split(":")
        self.m_nConn = MySQLdb.connect(
            host=szHost,
            port=int(port),
            user=cfg["user"],
            passwd=cfg["pwd"],
            db=cfg["db"],
            charset = 'utf8',
        )

        import dbs_opt_mp as dbs_opt
        while True:
            szSerial = workQueue.get()

            dictData = json.loads(szSerial)

            job = SyncJob()
            funObj = getattr(dbs_opt, dictData[dbs_def.IMP_FUN])

            szScene = dictData[dbs_def.SRC_SCENE]
            szSceneCbID = dictData[dbs_def.CB_ID]
            nSessionID = dictData[dbs_def.SESSION]
            param = dictData[dbs_def.PARAMS]
            job.Init(funObj, 0, nSessionID, szScene, szSceneCbID, param)
            dictRet = job.exe(self.m_nConn)
            if job.GetSceneName() is not None:
                dictRet[dbs_def.SESSION] = job.GetSession()
                dictRet[dbs_def.CB_ID] = job.GetCbID()
                retQueue.put((job.GetSceneName(), json.dumps(dictRet)))

    def Init(self):
        if self.m_bInited is True:
            return
        self.m_bInited = True

        self.m_dictChannel2Queue = {}
        self.m_dictChannel2QueueRet = {}
        for i in xrange(0, self.m_nQueueNum):
            self.m_dictChannel2Queue[i] = multiprocessing.Queue()
            self.m_dictChannel2QueueRet[i] = multiprocessing.Queue()

        for i in xrange(0, self.m_nQueueNum):
            p = multiprocessing.Process(target=self.worker, args=(i, self.m_dictChannel2Queue[i], self.m_dictChannel2QueueRet[0]), name="dbs@{0}".format(i))
            p.start()

        self.DispathWorkRet()

    def Add2JobQueue(self, nChannel, szSerial):
        nQueueID = nChannel % self.m_nQueueNum
        jobQueue = self.m_dictChannel2Queue[nQueueID]
        jobQueue.put(szSerial)

    def GenJob(self, dictSerial, szFunName):
        dictSerial[dbs_def.IMP_FUN] = szFunName
        nChannel = dictSerial[dbs_def.USE_CHANNEL]
        self.Add2JobQueue(nChannel, json.dumps(dictSerial))


_dbs = DbsMgr()
Add2JobQueue = _dbs.Add2JobQueue
GenJob = _dbs.GenJob
