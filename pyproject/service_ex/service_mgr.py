# -*- coding: utf-8 -*-
# @Author  : jh.feng

import sys
sys.path.append("./pyproject")

import wsurl.wsurl as wsurl
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
        import cluster_service_rsp as cluster_service_rsp
        cluster_service_rsp.SendMsg(socket, 8999, url)
        # socket.send(url)

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

def DispatchHttpServiceRequest():
    print("ServiceMgr.DispatchHttpServiceRequest")
    while True:
        gevent.sleep(0.01)
        GetUrlMgr().DispatchRequest()

if __name__ == "__main__":
    GetUrlMgr()
    gevent.spawn(DispatchHttpServiceRequest)

    import conf as conf
    conn_info = conf.dict_cfg["service_mgr"]["conn_info"]
    szAddr, szPort = conn_info.split(":")

    import setproctitle
    setproctitle.setproctitle("app_engine_service_mgr")
    server = StreamServer((szAddr, int(szPort)), handle)
    server.serve_forever()
