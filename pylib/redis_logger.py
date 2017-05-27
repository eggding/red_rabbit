import time
import datetime
import redis
import conf as conf

class LogMgr(object):
    def __init__(self):
        self.m_nOrder = 1
        szConnInfo = conf.dict_cfg["redis"]["conn_info"]
        szHost, szPort = szConnInfo.split(":")
        self.m_connPool = redis.ConnectionPool(host=szHost, port=int(szPort), max_connections=20)

    def LogInfo(self, szLogType, szLogKey, szLogContent):
        r = redis.Redis(connection_pool=self.m_connPool)
        r.hset(szLogType, szLogKey, szLogContent)

    def LogError(self, szLogContent):
        nTime = int(time.time())
        self.m_nOrder += 1
        szLogType = "trace_{0}".format(conf.dict_cfg["server_id"])
        szLogKey = "{0}_{1}".format(self.m_nOrder, datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S"))
        r = redis.Redis(connection_pool=self.m_connPool)
        r.hset(szLogType, szLogKey, szLogContent)

_LogMgr = LogMgr()

def GetLogMgr():
    return _LogMgr