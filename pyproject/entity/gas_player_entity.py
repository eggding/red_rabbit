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
        self.m_bIsResidual = False

        self.m_nCurRoomID = None

        self.m_nTotalPlayNum = 0

    def AddTotalPlayNum(self, nInc=1):
        self.m_nTotalPlayNum += nInc

    def GetTotalPlayNum(self):
        return self.m_nTotalPlayNum

    def SetResidual(self, bFlag):
        self.m_bIsResidual = bFlag

    def IsInResidualState(self):
        return self.m_bIsResidual

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
        self.m_nTotalPlayNum = dictData.get(PlayerPro.TOTAL_PLAY_NUM, 0)

        self.InitCompment(dictData)

    def GetPersistentDict(self):
        dictSerial = {
            PlayerPro.MONEY_LIST: self.m_PlayerMoneyMgr.Serial2List(),
            PlayerPro.TOTAL_PLAY_NUM: self.m_nTotalPlayNum,
        }
        return dictSerial


    def InitCompment(self, dictData):
        moneyMgr = compment_money.PlayerMoneyMgr(self)
        self.AddCompment(moneyMgr)
        moneyMgr.InitFromDict(dictData.get(PlayerPro.MONEY_LIST, {}))

    def IsMoneyEnough(self, nMoneyType, nNeedNum):
        return self.m_PlayerMoneyMgr.IsMoneyEnough(nMoneyType, nNeedNum)

    def AddMoney(self, nMoneyType, nAddNum, szReason):
        self.m_PlayerMoneyMgr.AddMoney(nMoneyType, nAddNum, szReason)

    def RequestChangeScene(self, szDstScene, dictExtra=None):
        if szDstScene == ff.service_name:
            return False

        if util.IsGasScene(szDstScene) is False:
            return False

        if self.GetRoomID() is not None:
            return False

        dictTmp = self.Serial2Dict()
        if dictExtra is not None:
            util.dict_merge(dictExtra, dictTmp)

        szSerial = json.dumps(dictTmp)
        entity_mgr.DelEntity(self.GetGlobalID())
        self.Destroy()
        ffext.change_session_scene(self.GetGlobalID(), szDstScene, szSerial)
        return True

    def GetWeChatInfo(self):
        return "test_wechat_info"

    def GetRandomName(self):
        a = u"比喻还可以突出事物的特征。因为比喻都是取整体上差异较大，而某一方面有共同性的事物来相比，喻体与本体相同之处往往就相当突出。因此，在比喻中，便常常有夸张的性质。如《硕鼠》，就其外形、生物的类别及其发展程度的高低而言，本体与喻体的差别是相当之大的；但是，在不劳而获这一点来说，却完全一致，所以这个比喻实际上是一种夸张的表现。"
        listTmp = []
        for i in xrange(0, len(a), 3):
            listTmp.append(a[i:i + 3])

        import random
        random.shuffle(listTmp)
        szName = ""
        nNum = random.randint(1, 3)
        for i in xrange(nNum):
            szName += listTmp[i]

        return szName

    def Serial2Client(self, rsp):
        rsp.player_id = self.GetGlobalID()
        if util.IsRobot(self.GetGlobalID()) is False:
            rsp.player_name = self.m_szName.encode("utf-8")
        else:
            rsp.player_name = self.GetRandomName().encode("utf-8")

        rsp.wechat_info = self.GetWeChatInfo().encode("utf-8")
        rsp.ip = self.ip.encode("utf-8")
        rsp.total_play_num = self.GetTotalPlayNum()

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

    def Persistent(self):
        # ffext.LOGINFO("FFSCENE_PYTHON", "Persistent {0}".format(self.GetGlobalID()))
        dictSerial = self.GetPersistentDict()
        dbs_client.DoAsynCall(rpc_def.DbsPersistentPlayerData, self.GetGlobalID(), json.dumps(dictSerial), nChannel=self.GetGlobalID())