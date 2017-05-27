# -*- coding: utf-8 -*-
# @Author  : jh.feng

import time
import conf as conf
import redis_logger as redis_logger

def LogInfo(nSession, szLogType, szLogContent):
    nTime = int(time.time())
    nServerID = conf.dict_cfg["server_id"]
    redis_logger.GetLogMgr().LogInfo("{0}_{1}".format(szLogType, nServerID), "{0}_{1}".format(nSession, nTime), szLogContent)

if __name__ == "__main__":
    dictTmp = {
        "a": "3948",
        "name": time.time(),
    }
    import json
    LogInfo(39844, "login", json.dumps(dictTmp))
