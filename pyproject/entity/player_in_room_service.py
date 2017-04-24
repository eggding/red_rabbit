# -*- coding: utf-8 -*-

import ffext
import rpc.rpc_def as rpc_def
import db.dbs_client as dbs_client
import db.dbs_def as dbs_def
from db.table.table_property_def import Player as PlayerPro
import proto.login_pb2 as login_pb2
import base_entity as base_entity
import compment.compment_money as compment_money

class RoomPlayer(base_entity.BaseEntity):
    def __init__(self):
        super(RoomPlayer, self).__init__()

        self.m_session = None
        self.m_szName = None
        self.m_nSex = 0
        self.m_GoldCoin = 0
        self.level      = 0
        self.exp        = 0
        self.online_time = 0
        self.ip         = None
        self.gate_name  = None

        self.m_nCurRoomID = None
        self.m_listSoulInRoom = None

    def GetGlobalID(self):
        return self.m_session

    def InitFromDict(self, dictDbRet):
        session = dictDbRet[dbs_def.SESSION]
        self.ip = dictDbRet[PlayerPro.IP]
        self.gate_name = dictDbRet[PlayerPro.GATE_NAME]

        dictData = dictDbRet[dbs_def.RESULT]
        self.m_session = int(session)
        self.m_szName = dictData[PlayerPro.NAME].encode("utf-8")
        self.m_nSex = int(dictData[PlayerPro.SEX])

        moneyMgr = compment_money.PlayerMoneyMgr(self)
        self.AddCompment(moneyMgr)
        moneyMgr.InitFromDict(dictData.get(PlayerPro.MONEY_LIST, {}))

    def Serial2Dict(self):
        dictSerial = {
            PlayerPro.IP: self.ip,
            PlayerPro.NAME: self.m_szName,
            PlayerPro.SEX: self.m_nSex,
        }
        return dictSerial

    def Serial2Client(self):
        syn_req = login_pb2.syn_player_data()
        syn_req.ret = 0
        syn_req.session = self.m_session
        syn_req.name = self.m_szName
        syn_req.sex = self.m_nSex
        syn_req.money_info = ""
        syn_req.bag_item_info = ""
        return syn_req.SerializeToString()

    def Persistent(self):
        ffext.LOGINFO("FFSCENE_PYTHON", "Persistent {0}".format(self.GetGlobalID()))
        dictSerial = {
            PlayerPro.MONEY_LIST: self.m_PlayerMoneyMgr.Serial2List()
        }

        import json
        dbs_client.DoAsynCall(rpc_def.DbsPersistentPlayerData, self.GetGlobalID(), json.dumps(dictSerial), nChannel=self.GetGlobalID())