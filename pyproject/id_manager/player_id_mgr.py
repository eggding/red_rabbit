# -*- coding: utf-8 -*-
# @Author  : jh.feng

import ffext, ff
import rpc.rpc_def as rpc_def
import db.dbs_client as dbs_client
import db.dbs_def as dbs_def
from util.enum_def import EIdType
import rpc.scene_def as scene_def

class idgen_t(object):
    def __init__(self, type_id_ = 0, server_id_ = 0):
        self.type_id = type_id_
        self.server_id = server_id_
        self.auto_inc_id = 0
        self.saving_flag = False
        self.runing_flag = 0
        self.m_bInit = False

    def RetGetIDAutoInc(self, dbRet):
        print("RetGetIDAutoInc ", dbRet)
        assert dbRet[dbs_def.FLAG] is True
        nAutoIncId, nRunningFlag = dbRet[dbs_def.RESULT]

        self.auto_inc_id = nAutoIncId
        self.runing_flag = nRunningFlag
        if self.runing_flag != 0:
            self.auto_inc_id += 500
            ffext.ERROR('last idgen shut down not ok, inc 50')

        if self.type_id == EIdType.eIdTypeRoom:
            if self.auto_inc_id < 100000:
                self.auto_inc_id = 100000
        else:
            if self.auto_inc_id < 65535:
                self.auto_inc_id = 65535
        self.m_bInit = True

    def init(self):
        # dbs_client.DoAsynCall(rpc_def.DbsGetIDData, 0, [self.type_id, self.server_id], funCb=self.RetGetIDAutoInc)
        pass

    def cleanup(self):
        assert False

    def gen_id(self):
        assert self.m_bInit is True
        assert ff.service_name == scene_def.DB_SERVICE_DEFAULT

        self.auto_inc_id += 1
        self.update_id()
        low16 = self.auto_inc_id & 0xFFFF
        high  = (self.auto_inc_id >> 16) << 32
        return high | (self.server_id << 16)| low16

    def dump_id(self, id_):
        low16 = id_ & 0xFFFF
        high  = id_ >> 32
        return high << 16 | low16

    def update_id(self):
        if self.saving_flag is True:
            return
        self.saving_flag = True
        now_val = self.auto_inc_id
        dbs_client.DoAsynCall(rpc_def.DbsUpdateID, 0, [now_val, self.type_id, self.server_id, now_val])

import conf as conf
_idMgr = idgen_t(EIdType.eIdTypePlayer, conf.dict_cfg["server_id"])
