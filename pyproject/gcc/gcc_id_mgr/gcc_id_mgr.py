# -*- coding: utf-8 -*-
# @Author  : jh.feng

import ffext
import rpc.rpc_def as rpc_def
import db.dbs_client as dbs_client
import db.dbs_def as dbs_def
from util.enum_def import EIdType, EDbsOptType
import db.dbs_common as dbs_common

class idgen_t(object):
    def __init__(self, type_id_ = 0, server_id_ = 0):
        self.type_id = type_id_
        self.server_id = server_id_
        self.auto_inc_id = 0
        self.saving_flag = False
        self.runing_flag = 0
        self.m_bInit = False
        self.init()

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
        dbs_client.DoAsynCall(rpc_def.DbsGetIDData, 0, [self.type_id, self.server_id], funCb=self.RetGetIDAutoInc)

    def cleanup(self):
        assert False

    def gen_id(self):
        assert self.m_bInit is True
        self.auto_inc_id += 1
        self.update_id()
        low16 = self.auto_inc_id & 0xFFFF
        high  = (self.auto_inc_id >> 16) << 32
        return high | (self.server_id << 16)| low16

    def gen_id_sector(self, nInc=1):
        assert self.m_bInit is True
        listRet = [self.auto_inc_id + 1, self.auto_inc_id + nInc]
        self.auto_inc_id += nInc
        self.update_id()
        return listRet

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

nServerID = 1
_PlayerIDMgr = idgen_t(EIdType.eIdTypePlayer, nServerID)
GenPlayerID = _PlayerIDMgr.gen_id

_roomIDMgr = idgen_t(EIdType.eIdTypeRoom, nServerID)
GenRoomIDSector = _roomIDMgr.gen_id_sector
