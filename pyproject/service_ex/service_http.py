# -*- coding: utf-8 -*-
# @Author  : jh.feng

import pycurl
import time
from cStringIO import StringIO
import urllib
import Queue
CURL_CACHE_NUM = 1000

from collections import namedtuple
HttpRequest = namedtuple('HttpRequest', ['id', 'type','url','data'])
HttpResponse = namedtuple('HttpResponse', ['id','isok', 'status_code', 'content'])

class HttpService(object):
    def __init__(self):
        self.m_bOpen = True
        self.m_listPoolCurl = []
        self.m_listFreeCurl = []
        self.m_multiCurl = pycurl.CurlMulti()
        self.InitCurlCache()

        self.m_jobQueue = Queue.Queue()
        self.m_retQueue = Queue.Queue()

    def InitCurlCache(self):
        for i in xrange(CURL_CACHE_NUM):
            c = pycurl.Curl()
            c.setopt(pycurl.FOLLOWLOCATION, 1)
            c.setopt(pycurl.MAXREDIRS, 5)
            c.setopt(pycurl.CONNECTTIMEOUT, 30)
            c.setopt(pycurl.TIMEOUT, 30)
            c.setopt(pycurl.NOSIGNAL, 1)
            c.setopt(pycurl.SSL_VERIFYPEER, 0)
            c.setopt(pycurl.SSL_VERIFYHOST, 0)
            self.m_listPoolCurl.append(c)
        self.m_listFreeCurl = self.m_listPoolCurl[:]

    def Response(self, response):
        self.m_retQueue.put(response)

    def GetRet(self):
        if self.m_retQueue.empty() is True:
            return None
        return self.m_retQueue.get()

    def run(self):
        print("start http service  ")
        self.m_beginTime = time.time()
        while self.m_bOpen:
            while self.m_listFreeCurl:
                try:
                    httpRequest = self.m_jobQueue.get(False)
                except Queue.Empty:
                    break
                c = self.m_listFreeCurl.pop()
                c.m_theStringIO = StringIO()
                c.setopt(pycurl.WRITEFUNCTION, c.m_theStringIO.write)
                c.setopt(pycurl.URL, httpRequest.url)
                c.m_httpRequest = httpRequest

                if httpRequest.type == "get":
                    c.setopt(pycurl.HTTPGET, 1)
                    c.setopt(pycurl.POST, 0)
                elif httpRequest.type == "post":
                    c.setopt(pycurl.HTTPGET, 0)
                    c.setopt(pycurl.POST, 1)
                    c.setopt(pycurl.POSTFIELDS, urllib.urlencode(httpRequest.data))
                self.m_multiCurl.add_handle(c)

            while self.m_bOpen:
                ret, num_handles = self.m_multiCurl.perform()
                if ret != pycurl.E_CALL_MULTI_PERFORM:
                    break

            while self.m_bOpen:
                num_q, ok_list, err_list = self.m_multiCurl.info_read()
                for c in ok_list:
                    self.m_multiCurl.remove_handle(c)
                    self.m_listFreeCurl.append(c)
                    response = HttpResponse(c.m_httpRequest.id,
                                                      True,
                                                      c.getinfo(pycurl.HTTP_CODE),
                                                      c.m_theStringIO.getvalue())
                    self.Response(response)
                for c, errno, errmsg in err_list:
                    self.m_multiCurl.remove_handle(c)
                    self.m_listFreeCurl.append(c)
                    response = HttpResponse(c.m_httpRequest.id,
                                                      False,
                                                      c.getinfo(pycurl.HTTP_CODE),
                                                      c.m_theStringIO.getvalue())
                    self.Response(response)
                if num_q == 0:
                    break
            # Currently no more I/O is pending, could do something in the meantime
            # (display a progress bar, etc.).
            # We just call select() to sleep until some more data is available.
            r = self.m_multiCurl.select(1.0)
            if r <= 0:
                time.sleep(0.03)

        print "exit"

_HttpService = HttpService()
