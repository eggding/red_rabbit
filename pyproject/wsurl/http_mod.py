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

def Test1(cb):
    szUrl = "https://g51-udataresys.nie.netease.com:8443/Recommender/FriendshipService?request=friendship_data&gameId=g51&token=tHAf25XUgM8Amfj&orderId=1852038034&server=1003&roleId=583a3c72353e9d0b47b92599&friends="
    GetUrlMgr().Get(szUrl, callback=cb)
