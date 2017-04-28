# -*- coding: utf-8 -*-
# @Author  : jh.feng

import json
import ffext, ff
import rpc.rpc_def as rpc_def
import db.dbs_client as dbs_client
import db.dbs_def as dbs_def
from db.table.table_property_def import Player as PlayerPro
import util.util as util
import base_entity as base_entity
import compment.compment_money as compment_money
import entity_mgr as entity_mgr

class GasPlayerEntity(base_entity.BaseEntity):
    def __init__(self):
        super(GasPlayerEntity, self).__init__()

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

    def SetRoomID(self, nRoomID):
        self.m_nCurRoomID = nRoomID

    def GetRoomID(self):
        return self.m_nCurRoomID

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

        self.InitCompment(dictData)

    def InitCompment(self, dictData):
        moneyMgr = compment_money.PlayerMoneyMgr(self)
        self.AddCompment(moneyMgr)
        moneyMgr.InitFromDict(dictData.get(PlayerPro.MONEY_LIST, {}))

    def RequestChangeScene(self, szDstScene, dictExtra=None):
        if szDstScene == ff.service_name:
            return False

        if util.IsGasScene(szDstScene) is False:
            return False

        dictTmp = self.Serial2Dict()
        if dictExtra is not None:
            util.dict_merge(dictExtra, dictTmp)

        szSerial = json.dumps(dictTmp)
        entity_mgr.DelEntity(self.GetGlobalID())
        self.Destroy()
        ffext.change_session_scene(self.GetGlobalID(), szDstScene, szSerial)
        return True

    def Serial2Dict(self):
        dictSerial = self.GetPersistentDict()
        dictSerial[PlayerPro.SESSION_ID] = self.GetGlobalID()
        dictSerial[PlayerPro.IP] = self.ip
        dictSerial[PlayerPro.NAME] = self.m_szName
        dictSerial[PlayerPro.SEX] = self.m_nSex
        dictSerial[PlayerPro.GATE_NAME] = self.gate_name
        return dictSerial

    def DeSerial(self, dictSerial):
        self.ip = dictSerial[PlayerPro.IP]
        self.m_szName = dictSerial[PlayerPro.NAME]
        self.m_nSex = dictSerial[PlayerPro.SEX]
        self.m_session = dictSerial[PlayerPro.SESSION_ID]
        self.gate_name = dictSerial[PlayerPro.GATE_NAME]
        self.InitCompment(dictSerial)

    def GetPersistentDict(self):
        dictSerial = {
            PlayerPro.MONEY_LIST: self.m_PlayerMoneyMgr.Serial2List()
        }
        return dictSerial

    def Persistent(self):
        ffext.LOGINFO("FFSCENE_PYTHON", "Persistent {0}".format(self.GetGlobalID()))
        dictSerial = self.GetPersistentDict()
        dbs_client.DoAsynCall(rpc_def.DbsPersistentPlayerData, self.GetGlobalID(), json.dumps(dictSerial), nChannel=self.GetGlobalID())