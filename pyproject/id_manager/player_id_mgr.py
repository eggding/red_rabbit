# -*- coding: utf-8 -*-
# @Author  : jh.feng

import ffext, ff
import rpc.rpc_def as rpc_def
import db.dbs_client as dbs_client
import db.dbs_def as dbs_def
from util.enum_def import EIdType, EDbsOptType
import rpc.scene_def as scene_def
import dbs_common as dbs_common

class idgen_t(object):
    def __init__(self, type_id_ = 0, server_id_ = 0):
        self.type_id = type_id_
        self.server_id = server_id_
        self.auto_inc_id = 0
        self.saving_flag = False
        self.runing_flag = 0
        self.m_bInit = False

    def RetGetIDAutoInc(self, dbRet):
        # print("RetGetIDAutoInc ", dbRet)
        assert dbRet[dbs_def.FLAG] is True
        nAutoIncId, nRunningFlag = dbRet[dbs_def.RESULT]

        self.auto_inc_id = nAutoIncId
        self.runing_flag = nRunningFlag
        if self.runing_flag != 0:
            self.auto_inc_id += 50
            ffext.ERROR('last idgen shut down not ok, inc 50')

        if self.type_id == EIdType.eIdTypeRoom:
            if self.auto_inc_id < 100000:
                self.auto_inc_id = 100000
        else:
            if self.auto_inc_id < 100:
                self.auto_inc_id = 100
        self.m_bInit = True

    def ImpGetIDData(self, conn):
        dictRet = {dbs_def.FLAG: True}
        nTypeID, nServerID = self.type_id, self.server_id
        sql = "SELECT `AUTO_INC_ID`, `RUNING_FLAG` FROM `id_generator` WHERE `TYPE` = '%d' AND `SERVER_ID` = '%d'" % (nTypeID, nServerID)
        ret = dbs_common.SyncQueryTrans(EDbsOptType.eQuery, conn, sql)
        if len(ret) == 0:
            # 数据库中还没有这一行，插入
            sql = "INSERT INTO `id_generator` SET `AUTO_INC_ID` = '0',`TYPE` = '%d', `SERVER_ID` = '%d', `RUNING_FLAG` = '1' " % (nTypeID, nServerID)
            assert dbs_common.SyncQueryTrans(EDbsOptType.eInsert, conn, sql) is not None
            dictRet[dbs_def.RESULT] = [0, 1]
            return dictRet

        sql = "UPDATE `id_generator` SET `RUNING_FLAG` = '1' WHERE `TYPE` = '%d' AND `SERVER_ID` = '%d'" % (nTypeID, nServerID)
        assert dbs_common.SyncQueryTrans(EDbsOptType.eUpdate, conn, sql) is not None
        dictRet[dbs_def.RESULT] = ret[0]
        return dictRet

    def ImpUpdateID(self, conn, listData):
        now_val, type_id, server_id, now_val = listData
        sql = "UPDATE `id_generator` SET `AUTO_INC_ID` = '%d' WHERE `TYPE` = '%d' AND `SERVER_ID` = '%d' AND `AUTO_INC_ID` < '%d'" % (now_val, type_id, server_id, now_val)
        assert dbs_common.SyncQueryTrans(EDbsOptType.eUpdate, conn, sql) is not None
        dictSerial = {dbs_def.FLAG: True}
        return dictSerial

    def init(self, conn):
        dictRet = self.ImpGetIDData(conn)
        self.RetGetIDAutoInc(dictRet)

    def cleanup(self):
        assert False

    def gen_id(self, conn):
        assert ff.service_name == scene_def.DB_SERVICE_DEFAULT
        if self.m_bInit is False:
            self.init(conn)

        self.auto_inc_id += 1
        self.update_id(conn)
        low16 = self.auto_inc_id & 0xFFFF
        high  = (self.auto_inc_id >> 16) << 32
        return high | (self.server_id << 16)| low16

    def dump_id(self, id_):
        low16 = id_ & 0xFFFF
        high  = id_ >> 32
        return high << 16 | low16

    def update_id(self, conn):
        if self.saving_flag is True:
            return
        self.saving_flag = True
        now_val = self.auto_inc_id
        self.ImpUpdateID(conn, [now_val, self.type_id, self.server_id, now_val])

import conf as conf
_idMgr = idgen_t(EIdType.eIdTypePlayer, conf.dict_cfg["server_id"])
GenPlayerID = _idMgr.gen_id
