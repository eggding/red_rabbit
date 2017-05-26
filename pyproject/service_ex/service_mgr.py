# -*- coding: utf-8 -*-
# @Author  : jh.feng

import wsurl.wsurl as wsurl
import sys
sys.path.append("./pyproject")

import gevent as gevent
import service_http as service_http
from gevent.server import StreamServer

g_urlMgr = None
g_nMaxRecvData = 4096 * 10

def GetUrlMgr():
    global g_urlMgr
    if g_urlMgr is None:
        g_urlMgr = wsurl.WsUrl(1)
        g_urlMgr.Start()
    return g_urlMgr

def HandleMsg(szMsg, socket, addr):
    print("recv from ", addr, szMsg)
    url = "https://github.com/gevent/gevent"

    def _OnRet(httpRsp):
        print(httpRsp)
        socket.send(httpRsp.content)

    print("make http req ", url)
    GetUrlMgr().Get(url, _OnRet)

def HandleClose(socket, address):
    print("on conn close ", address)

def handle(socket, address):
    print("connect come ", address)
    while True:
        try:
            szMsg = socket.recv(g_nMaxRecvData)
            HandleMsg(szMsg, socket, address)
        except:
            HandleClose(socket, address)
            socket.close()
            return

def DispatchRequest():
    while True:
        gevent.sleep(0.1)
        GetUrlMgr().DispatchRequest()

gevent.spawn(DispatchRequest)

server = StreamServer(('127.0.0.1', 5000), handle)
server.serve_forever()
