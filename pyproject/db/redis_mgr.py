# -*- coding: utf-8 -*-
# @Author  : jh.feng

import redis
import db.table.table_property_def as table_property_def

class RedisMgr(object):
    def __init__(self):
        self.m_pool = redis.ConnectionPool(host='127.0.0.1', port=6379)
        self.m_conn = redis.Redis(connection_pool=self.m_pool)

    def UpdateMoney(self, nPlayerGID, szTable, listMoney):
        szMainKey = "{0}_{1}".format(nPlayerGID, szTable)
        for tupleData in listMoney:
            nMoneyType, nValue = tupleData
            szSubKey = str(nMoneyType)
            self.m_conn.hset(szMainKey, szSubKey, nValue)

    def exe(self, nPlayerGID, dictSerial):
        pipe = self.m_conn.pipeline(transaction=True)
        listMoney = dictSerial.get(table_property_def.Player.MONEY_LIST)
        if listMoney is not None:
            self.UpdateMoney(nPlayerGID, table_property_def.TableName.PLAYER_MONEY, listMoney)
        pipe.execute()
