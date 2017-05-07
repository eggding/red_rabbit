# -*- coding:utf-8 -*-
import random, time
import json
import ffext
import Queue as queue
import rpc.rpc_def as rpc_def
import dbs_def as dbs_def


class AsynJob(object):
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
        self.m_funObj(dbsConn, self)

class DbsMgr(object):
    def __init__(self):
        self.m_nNumDbConn = 3
        self.m_nQueueNum = 70
        self.m_listConnChannel = []
        self.m_dictChannel2Queue = {}
        self.m_dictQueueWorkStatus = {}
        self.m_dictQueueWorkTime = {}
        self.m_nCount = 1
        self.m_nPreTime = time.clock()
        self.m_bInited = False

    def RandomChoose(self):
        nRanQueue = random.randint(0, self.m_nQueueNum - 1)
        if self.m_dictQueueWorkStatus[nRanQueue] is False:
            if self.m_dictChannel2Queue[nRanQueue].empty() is False:
                return nRanQueue
        return None

    def ChooseMaxLen(self):
        nDstQueue = None
        nQueueSize = None
        for nQueueID, bIsWorking in self.m_dictQueueWorkStatus.iteritems():
            if bIsWorking is True:
                continue

            queueObj = self.m_dictChannel2Queue[nQueueID]
            if queueObj.empty() is True:
                continue
            if nQueueSize is None or nQueueSize < queueObj.qsize():
                nQueueSize = queueObj.qsize()
                nDstQueue = nQueueID
        return nDstQueue

    def CheckWorkTime(self, a):
        ffext.once_timer(3000, self.CheckWorkTime, 1)
        nGap = 5 * 1000
        for nQueueID, nTime in self.m_dictQueueWorkTime.iteritems():
            queueObj = self.m_dictChannel2Queue[nQueueID]
            if queueObj.qsize() == 0:
                continue

            if nTime + nGap > time.time():
                continue
            ffext.ERROR('queue {0} running too long, should it blocking? {1}'.format(nQueueID, self.DumpDbQueue()))

    def DispathJob(self, a):
        ffext.once_timer(200, self.DispathJob, 1)

        nDstQueue = self.RandomChoose()
        if nDstQueue is None:
            nDstQueue = self.ChooseMaxLen()

        if nDstQueue is not None:
            self.GrapJobFromQueue(nDstQueue)

    def Init(self):
        import conf as conf
        dictDbCfg = conf.dict_cfg["dbs"]

        # channel
        self.m_dictChannel2Queue = {}
        self.m_dictQueueWorkStatus = {}
        for i in xrange(0, self.m_nNumDbConn):
            dbServiceObj = ffext.ffdb_create('mysql://{0}/{1}/{2}/{3}'.format(dictDbCfg["host"], dictDbCfg["user"], dictDbCfg["pwd"], dictDbCfg["db"]))
            assert dbServiceObj is not None
            self.m_listConnChannel.append(dbServiceObj)

        for i in xrange(0, self.m_nQueueNum):
            self.m_dictChannel2Queue[i] = queue.Queue()
            self.m_dictQueueWorkStatus[i] = False
            self.m_dictQueueWorkTime[i] = time.time()

        self.m_bInited = True
        # self.DispathJob(1)
        self.CheckWorkTime(1)

    def DumpDbQueue(self):
        dictQueueJobNum = {}
        for nChannelID, queueObj in self.m_dictChannel2Queue.iteritems():
            if queueObj.qsize() != 0:
                dictQueueJobNum[nChannelID] = queueObj.qsize()

        if len(dictQueueJobNum) == 0:
            return None
        return json.dumps(dictQueueJobNum)

    def OnOneDbQueryDone(self, dbRet, job):

        szDumpData = self.DumpDbQueue()
        if szDumpData is not None:
            ffext.LOGINFO("FFSCENE_PYTHON", "DbsMgr.OnOneDbQueryDone {0}".format(szDumpData))

        if isinstance(dbRet, ffext.query_result_t):
            dictSerial = {
                dbs_def.FLAG: dbRet.flag,
                dbs_def.COL: dbRet.column,
                dbs_def.RESULT: dbRet.result,
            }
        else:
            dictSerial = dbRet

        if job.GetSceneName() is not None:
            dictSerial[dbs_def.SESSION] = job.GetSession()
            dictSerial[dbs_def.CB_ID] = job.GetCbID()
            ffext.call_service(job.GetSceneName(), rpc_def.OnDbAsynCallReturn, json.dumps(dictSerial))

        if job.GetQueueID() is not None:
            self.m_dictQueueWorkStatus[job.GetQueueID()] = False
            self.m_dictQueueWorkTime[job.GetQueueID()] = time.time()

        nDstQueue = self.RandomChoose()
        if nDstQueue is None:
            nDstQueue = self.ChooseMaxLen()
        if nDstQueue is not None:
            self.GrapJobFromQueue(nDstQueue)

    def GrapJobFromQueue(self, nQueueID):
        jobQueue = self.m_dictChannel2Queue[nQueueID]
        if jobQueue.empty() is True:
            return

        if self.m_dictQueueWorkStatus[nQueueID] is True:
            return

        nConnID = nQueueID % self.m_nNumDbConn
        self.m_dictQueueWorkStatus[nQueueID] = True
        self.m_dictQueueWorkTime[nQueueID] = time.time()
        jobQueue.get(timeout=1).exe(self.m_listConnChannel[nConnID])

    def Add2JobQueue(self, szSrcScene, cb_id, nSessionID, nChannel, funObj, param=None):
        if self.m_bInited is False:
            self.Init()

        nQueueID = nChannel % self.m_nQueueNum
        job = AsynJob()
        job.Init(funObj, nQueueID, nSessionID, szSrcScene, cb_id, param)
        jobQueue = self.m_dictChannel2Queue[nQueueID]
        jobQueue.put(job)
        self.GrapJobFromQueue(nQueueID)

    def GenJob(self, dictSerial, funObj):
        szScene = dictSerial[dbs_def.SRC_SCENE]
        szSceneCbID = dictSerial[dbs_def.CB_ID]
        nSessionID = dictSerial[dbs_def.SESSION]
        nChannel = dictSerial[dbs_def.USE_CHANNEL]
        param = dictSerial[dbs_def.PARAMS]
        self.Add2JobQueue(szScene, szSceneCbID, nSessionID, nChannel, funObj, param)


_dbs = DbsMgr()
OnOneDbQueryDone = _dbs.OnOneDbQueryDone
Add2JobQueue = _dbs.Add2JobQueue
GenJob = _dbs.GenJob
