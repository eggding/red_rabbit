# -*- coding: utf-8 -*-
# @Author  : jh.feng

import time
import redis
import conf as conf

class LogMgr(object):
    def __init__(self):
        szConnInfo = conf.dict_cfg["redis"]["conn_info"]
        szHost, szPort = szConnInfo.split(":")
        self.m_connPool = redis.ConnectionPool(host=szHost, port=int(szPort), max_connections=20)

    def LogInfo(self, szLogType, szLogKey, szLogContent):
        r = redis.Redis(connection_pool=self.m_connPool)
        r.hset(szLogType, szLogKey, szLogContent)

_LogMgr = LogMgr()

def LogInfo(nSession, szLogType, szLogContent):
    nTime = int(time.time())
    nServerID = conf.dict_cfg["server_id"]
    _LogMgr.LogInfo("{0}_{1}".format(szLogType, nServerID), "{0}_{1}".format(nSession, nTime), szLogContent)

if __name__ == "__main__":
    dictTmp = {
        "a": "3948",
        "name": time.time(),
    }
    import json
    LogInfo(39844, "login", json.dumps(dictTmp))
