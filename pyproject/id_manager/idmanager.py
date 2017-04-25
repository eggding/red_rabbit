# -*- coding: utf-8 -*-
import ffext
from util.enum_def import EIdType

class idgen_t(object):
    def __init__(self, db_host_, type_id_ = 0, server_id_ = 0):
        self.type_id = type_id_
        self.server_id = server_id_
        self.auto_inc_id = 0
        self.db_host = db_host_
        self.db      = None
        self.saving_flag = False
        self.runing_flag = 0
        self.m_bInit = False

    def init(self, conn):
        self.m_bInit = True

        ret = conn.sync_query("SELECT `AUTO_INC_ID`, `RUNING_FLAG` FROM `id_generator` WHERE `TYPE` = '%d' AND `SERVER_ID` = '%d'" % (self.type_id, self.server_id))
        #print(ret.flag, ret.result, ret.column)
        if len(ret.result) == 0:
            #数据库中还没有这一行，插入
            conn.sync_query("INSERT INTO `id_generator` SET `AUTO_INC_ID` = '0',`TYPE` = '%d', `SERVER_ID` = '%d', `RUNING_FLAG` = '1' " % (self.type_id, self.server_id))
            return True
        else:
            self.auto_inc_id = int(ret.result[0][0])
            self.runing_flag = int(ret.result[0][1])
            if self.runing_flag != 0:
                self.auto_inc_id += 50
                ffext.ERROR('last idgen shut down not ok, inc 50')
            conn.sync_query("UPDATE `id_generator` SET `RUNING_FLAG` = '1' WHERE `TYPE` = '%d' AND `SERVER_ID` = '%d'" % (self.type_id, self.server_id))

        if self.type_id == EIdType.eIdTypeRoom:
            if self.auto_inc_id < 100000:
               self.auto_inc_id = 100000
        else:
            if self.auto_inc_id < 65535:
               self.auto_inc_id = 65535
        return True

    def cleanup(self):
        db = ffext.ffdb_create(self.db_host)
        now_val = self.auto_inc_id
        db.sync_query("UPDATE `id_generator` SET `AUTO_INC_ID` = '%d', `RUNING_FLAG` = '0' WHERE `TYPE` = '%d' AND `SERVER_ID` = '%d'" % (now_val, self.type_id, self.server_id))
        return True

    def gen_id(self, conn):
        if self.m_bInit is False:
            self.init(conn)

        self.auto_inc_id += 1
        self.update_id(conn)
        low16 = self.auto_inc_id & 0xFFFF
        high  = (self.auto_inc_id >> 16) << 32
        return high | (self.server_id << 16)| low16

    def gen_id_sector(self, conn, nInc=1):
        if self.m_bInit is False:
            self.init(conn)

        listRet = [self.auto_inc_id + 1, self.auto_inc_id + nInc]
        self.auto_inc_id += nInc
        self.update_id(conn)
        return listRet


    def dump_id(self, id_):
        low16 = id_ & 0xFFFF
        high  = id_ >> 32
        return high << 16 | low16

    def update_id(self, conn):
        if True == self.saving_flag:
            return
        self.saving_flag = True
        now_val = self.auto_inc_id
        def cb(ret):
            #print(ret.flag, ret.result, ret.column)
            self.saving_flag = False
            if now_val < self.auto_inc_id:
                self.update_id(conn)
        conn.query("UPDATE `id_generator` SET `AUTO_INC_ID` = '%d' WHERE `TYPE` = '%d' AND `SERVER_ID` = '%d' AND `AUTO_INC_ID` < '%d'" % (now_val, self.type_id, self.server_id, now_val), cb)
        return

nServerID = 1
_PlayerIDMgr = idgen_t("", EIdType.eIdTypePlayer, nServerID)
GenPlayerID = _PlayerIDMgr.gen_id

_roomIDMgr = idgen_t("", EIdType.eIdTypeRoom, nServerID)
GenRoomIDSector = _roomIDMgr.gen_id_sector
