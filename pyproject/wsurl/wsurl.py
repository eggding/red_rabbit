# -*- coding: utf-8 -*-
# @Time    : 2016/12/12 18:16
# @Author  : jh.feng

import Queue
import wsurl_thread as wsurl_thread
import wsurl_def as wsurl_def
import util.tick_mgr as tick_mgr


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
        self.RegTick()

    def RegTick(self):
        self.UnRegTick()
        self.m_tickUpdate = tick_mgr.RegisterOnceTick(456, self.DispatchRequest)

    def UnRegTick(self):
        if self.m_tickUpdate is not None:
            tick_mgr.UnRegisterOnceTick(self.m_tickUpdate)
            self.m_tickUpdate=None

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
            print("Test cb")
            if cb:
                cb(httpReponse)

g_job=0
gtime=0


def Test1():
    global g_job,gtime
    import time
    nTotalJobs=20000

    def t(self):
        pass

    WsUrl.RegTick=t

    w=WsUrl()
    w.Start()



    def callback1(httpReponse):
        global g_job,gtime

        g_job+=1
        if g_job>=20000:
            print ("success" ,g_job,20000/(time.time()-gtime),len(httpReponse.content))
            w.Stop()

    #url="https://g51-udataresys.nie.netease.com:8443/Recommender/FriendshipService?request=friendship_data&gameId=g51&token=tHAf25XUgM8Amfj&orderId=1852038034&server=1003&roleId=583a3c72353e9d0b47b92599&friends="
    #url = "http://img3.126.net/kaola/dsp1e/img/short.png"
    url = "http://g51-udataresys.nie.netease.com/Recommender/FriendshipService?request=friendship_data&gameId=g51&token=tHAf25XUgM8Amfj&orderId=1852038034&server=1005&roleId=123&friends="
    #url = "http://www.mi.com"

    for i in xrange(20000):
        w.Get(url,callback1)


    gtime=time.time()
    #print "lldsss",w.m_queueJob.qsize()
    #w.m_listThread[0].run()



    while w.m_bOpen:
        w.DispatchRequest()
        time.sleep(0.1)


def Test2():

    import time

    def t(self):
        pass

    WsUrl.RegTick=t
    w=WsUrl()
    w.Start()

    def callback1(httpReponse):
        print("rsp cb 1 ")

    #url="https://g51-udataresys.nie.netease.com:8443/Recommender/FriendshipService?request=friendship_data&gameId=g51&token=tHAf25XUgM8Amfj&orderId=1852038034&server=1003&roleId=583a3c72353e9d0b47b92599&friends="
    url = "http://img3.126.net/kaola/dsp1e/img/short.png"
    #url = "http://g51-udataresys.nie.netease.com/Recommender/FriendshipService?request=friendship_data&gameId=g51&token=tHAf25XUgM8Amfj&orderId=1852038034&server=1005&roleId=123&friends="
    #url = "http://www.mi.com"

    while w.m_bOpen:
        for i in xrange(1):
            w.Get(url,callback1)

        w.DispatchRequest()
        time.sleep(1)

def Test3():
    import time
    geturl = "http://g51-udataresys.nie.netease.com/Recommender/FriendshipService?request=friendship_data&gameId=g51&token=tHAf25XUgM8Amfj&orderId=1852038034&server=1005&roleId=123&friends="
    def c(b):
        if b.content == '{"response":"friendship_data","status":"not_exists","success":false}':
            pass
            #print "get True"
        else:
            print "get False"

    def p(b):
        if b.content=='{\n  "args": {}, \n  "data": "", \n  "files": {}, \n  "form": {\n    "c": "2", \n    "d": "1"\n  }, \n  "headers": {\n    "Accept": "*/*", \n    "Content-Length": "7", \n    "Content-Type": "application/x-www-form-urlencoded", \n    "Host": "httpbin.org", \n    "User-Agent": "PycURL/7.43.0 libcurl/7.47.0 OpenSSL/1.0.2e zlib/1.2.8 c-ares/1.10.0 libssh2/1.6.0"\n  }, \n  "json": null, \n  "origin": "43.230.90.94", \n  "url": "http://httpbin.org/post"\n}\n':
            pass

#            print "post True"
        else:
            print "post False"

    posturl="http://httpbin.org/post"
    postdata={"d":1,"c":2}

    def t(self):
        pass
    WsUrl.RegTick=t
    w=WsUrl()
    w.Start()

    while w.m_bOpen:
        for i in xrange(20):
            w.Post(posturl,p,postdata)
            w.Get(geturl,c)
            w.Post(posturl,p,postdata)
            w.Get(geturl,c)

        w.DispatchRequest()
        time.sleep(1)

if __name__ == '__main__':
    Test3()