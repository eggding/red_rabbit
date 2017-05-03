# coding=UTF-8

import ffext as framework
import compment.base_compment as base_compment

class PlayerMoneyMgr(base_compment.BaseCompment):
    def __init__(self, owner):
        super(PlayerMoneyMgr, self).__init__(owner, "m_PlayerMoneyMgr")

        self.m_dictType2Money = {}

    def OnDestroy(self):
        print("m_PlayerMoneyMgr OnDestroy")

    def InitFromDict(self, listMoneyData):
        self.m_dictType2Money = {}
        for moneyType, nMoneyValue in listMoneyData:
            self.m_dictType2Money[moneyType] = nMoneyValue

    def IsMoneyEnough(self, nMoneyType, nNeedNum):
        nHaveMoney = self.m_dictType2Money.get(nMoneyType, 0)
        return nHaveMoney >= nNeedNum

    def SerialAllMoney(self):
        import json
        return json.dumps(self.m_dictType2Money)

    def AddMoney(self, nMoneyType, nAdd, szReason):
        if nAdd >= 0:
            self.m_dictType2Money[nMoneyType] = self.m_dictType2Money.get(nMoneyType, 0) + nAdd
        else:
            assert self.m_dictType2Money.get(nMoneyType, 0) >= nAdd
            self.m_dictType2Money[nMoneyType] += nAdd

        framework.LOGINFO("FFSCENE_PYTHON", "AddMoney {0} {1} {2} {3}".format(self.GetOwner().GetGlobalID(), nAdd, self.SerialAllMoney(), szReason))

    def Serial2List(self):
        listRet = []
        for nType, nVal in self.m_dictType2Money.iteritems():
            listRet.append((nType, nVal))
        return listRet