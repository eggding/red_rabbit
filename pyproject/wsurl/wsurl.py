# -*- coding: utf-8 -*-
# @Time    : 2016/12/12 18:16
# @Author  : jh.feng

import Queue
import wsurl_thread as wsurl_thread
import wsurl_def as wsurl_def

class WsUrl(object):
    def __init__(self,nThreadNum=1):
        self.m_nThreadNum=nThreadNum
        self.m_queueJob=Queue.Queue() # wsurl_def.HttpRequest
        self.m_queueResult=Queue.Queue() # wsurl_def.HttpResponse

        self.m_listThread=[]
        self.m_bOpen=False
        self.m_nJobID = 0  #  auto id
        self.m_dictJobID2Callback = {} #id->callback
        self.m_dictCallback2IDS = {} # callback -> set( ids)
        self.m_tickUpdate=None
    #     self.RegTick()
    #
    # def RegTick(self):
    #     self.m_tickUpdate = tick_mgr.RegisterOnceTick(456, self.DispatchRequest)

    # def UnRegTick(self):
    #     if self.m_tickUpdate is not None:
    #         tick_mgr.UnRegisterOnceTick(self.m_tickUpdate)
    #         self.m_tickUpdate=None

    def GenJobID(self):
        self.m_nJobID += 1
        return self.m_nJobID

    def AddJob(self, callback, szType,url,data=None):
        nJobID = self.GenJobID()
        httpRequest = wsurl_def.HttpRequest(nJobID,szType,url,data)
        self.m_dictJobID2Callback[nJobID] = callback
        self.m_dictCallback2IDS.setdefault(callback,set([]))
        self.m_dictCallback2IDS[callback].add(nJobID)
        self.m_queueJob.put(httpRequest)
        return nJobID

    def RemoveJob(self, nJobID):
        callback = self.m_dictJobID2Callback.pop(nJobID, None)
        if callback in self.m_dictCallback2IDS:
            self.m_dictCallback2IDS[callback].discard(nJobID)
            if not self.m_dictCallback2IDS[callback]:
                del self.m_dictCallback2IDS[callback]

        return callback

    def RemoveJobsByCallback(self, callback):
        if callback in self.m_dictCallback2IDS:
            for nCallbackID in self.m_dictCallback2IDS[callback]:
                self.m_dictJobID2Callback.pop(nCallbackID, None)
            del self.m_dictCallback2IDS[callback]

    def Get(self,url, callback):
        self.AddJob(callback,'get',url)

    def Post(self,url,callback,data):
        self.AddJob(callback,'post',url,data)


    def Start(self):
        if self.m_bOpen:
            return
        self.m_bOpen=True
        for i in xrange(self.m_nThreadNum):
            self.m_listThread.append(wsurl_thread.WsUrlThread(self))

        for thread in self.m_listThread:
            thread.start()

    def Stop(self):
        if not self.m_bOpen:
            return
        self.m_bOpen=False

        for thread in self.m_listThread:
            thread.join()

        self.m_listThread=[]

    def DispatchRequest(self):
        while self.m_bOpen:
            try:
                httpReponse = self.m_queueResult.get(False)
            except Queue.Empty:
                break
            cb = self.RemoveJob(httpReponse.id)
            if cb:
                cb(httpReponse)

g_job=0
gtime=0

