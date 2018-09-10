# -*- coding: utf-8 -*-
# @Author  : jh.feng

import wsurl as wsurl
g_urlMgr = None

def GetUrlMgr():
    global g_urlMgr
    if g_urlMgr is None:
        g_urlMgr = wsurl.WsUrl(1)
        g_urlMgr.Start()
    return g_urlMgr
