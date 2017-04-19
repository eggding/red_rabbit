# coding=UTF-8
from util.enum_def import EMoneyType
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

        import random
        if len(self.m_dictType2Money) == 0:
            self.m_dictType2Money[EMoneyType.eYuanbao] = random.randint(1, 10494)
        else:
            self.m_dictType2Money[EMoneyType.eYuanbao] = random.randint(23, 498444)

    def Serial2List(self):
        listRet = []
        for nType, nVal in self.m_dictType2Money.iteritems():
            listRet.append((nType, nVal))
        return listRet