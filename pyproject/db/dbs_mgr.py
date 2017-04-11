# -*- coding:utf-8 -*-

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
        self.m_listConnChannel = []
        self.m_dictChannel2Queue = {}
        self.m_bInited = False

    def Init(self):
        import conf as conf
        dictDbCfg = conf.dict_cfg["dbs"]

        # channel
        self.m_dictChannel2Queue = {}
        for i in xrange(0, self.m_nNumDbConn):
            dbServiceObj = ffext.ffdb_create('mysql://{0}/{1}/{2}/{3}'.format(dictDbCfg["host"], dictDbCfg["user"], dictDbCfg["pwd"], dictDbCfg["db"]))
            assert dbServiceObj is not None
            self.m_listConnChannel.append(dbServiceObj)
            self.m_dictChannel2Queue[i] = queue.Queue()

        self.m_bInited = True

    def OnOneDbQueryDone(self, dbRet, job):
        if isinstance(dbRet, dict):
            dictSerial = dbRet
        else:
            dictSerial = {
                dbs_def.FLAG: dbRet.flag,
                # dbs_def.COL: dbRet.column,
                dbs_def.RESULT: dbRet.result,
            }

        dictSerial[dbs_def.SESSION] = job.GetSession()
        dictSerial[dbs_def.CB_ID] = job.GetCbID()
        ffext.call_service(job.GetSceneName(), rpc_def.OnDbAsynCallReturn, json.dumps(dictSerial))

        nQueueID = job.GetQueueID()
        if nQueueID is not None and not self.m_dictChannel2Queue[nQueueID].empty():
            self.GrapJobFromQueue(nQueueID)

    def GrapJobFromQueue(self, nQueueID):
        jobQueue = self.m_dictChannel2Queue[nQueueID]
        jobQueue.get().exe(self.m_listConnChannel[nQueueID])

    def Add2JobQueue(self, szSrcScene, cb_id, nSession, funObj, param=None):
        if self.m_bInited is False:
            self.Init()

        nQueueID = int(nSession) % self.m_nNumDbConn
        jobQueue = self.m_dictChannel2Queue[nQueueID]
        bEmpty = jobQueue.empty()
        job = AsynJob()
        job.Init(funObj, nQueueID, nSession, szSrcScene, cb_id, param)
        jobQueue.put(job)
        if bEmpty:
            self.GrapJobFromQueue(nQueueID)

_dbs = DbsMgr()
OnOneDbQueryDone = _dbs.OnOneDbQueryDone
Add2JobQueue = _dbs.Add2JobQueue

