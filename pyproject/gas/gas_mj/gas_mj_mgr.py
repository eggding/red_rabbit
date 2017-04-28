# -*- coding: utf-8 -*-
# @Author  : jh.feng

import ffext
import json
import random
from util.enum_def import EGameRule
import entity.rule_base as rule_base

class GasMjRule(rule_base.GameRuleBase):
    def __init__(self, roomObj):
        super(GasMjRule, self).__init__(EGameRule.eGameRuleMj)

        self.m_roomObj = roomObj
        self.m_dictCfg = None

        self.m_nMemberNum = roomObj.GetMemberNum()

        # 局数
        self.m_nCurJu = 0

        # 当前第几轮
        self.m_nTurnNum = 0

        # 庄家
        self.m_nZhuang = 0

        # 轮到当前为那个玩家
        self.m_nCurOptMember = 1

        # 当前摸到第几个牌
        self.m_nNextCardIndex = 0

        # 牌序
        self.m_listGlobalCard = []

        # 每个玩家的牌
        self.m_dictPosCarList = {}

    def InitDefault(self):
        self.m_nTurnNum = 0
        self.m_nZhuang = 0

        self.m_nCurOptMember = 1
        self.m_nNextCardIndex = 0
        self.m_listGlobalCard = []

        listRoomMember = self.m_roomObj.GetMemberList()
        nNum = len(listRoomMember)
        for nPos in xrange(1, nNum + 1):
            self.m_dictPosCarList[nPos] = []

    def GetMaxJuNum(self):
        return self.m_dictCfg.get("chang_shu", 1) * self.m_dictCfg.get("ju_for_chang", 5)

    def InitWithCfg(self, dictCfg):
        self.m_dictCfg = dictCfg

    def DingZhuang(self):
        """
        定庄
        :return:
        """
        listRoomMember = self.m_roomObj.GetMemberList()
        nRoomMemberNum = len(listRoomMember)
        assert nRoomMemberNum in (2, 4)
        nZhuang = listRoomMember[random.randint(0, nRoomMemberNum - 1)]
        self.m_nZhuang = nZhuang
        ffext.LOGINFO("FFSCENE_PYTHON", "GasMj.DingZhuang {0}".format(nZhuang))

    def XiPai(self):
        nMaxCarNum = 134
        self.m_listGlobalCard = []
        for i in xrange(1, nMaxCarNum + 1):
            self.m_listGlobalCard.append(i)

        nLen = nMaxCarNum - 1
        while nLen > 0:
            nPos = random.randint(0, nLen)
            nTmpVal = self.m_listGlobalCard[nLen]
            self.m_listGlobalCard[nLen] = self.m_listGlobalCard[nPos]
            self.m_listGlobalCard[nPos] = nTmpVal
            nLen -= 1

        ffext.LOGINFO("FFSCENE_PYTHON", "GasMj.XiPai {0}".format(json.dumps(self.m_listGlobalCard)))

    def GetNextPos(self):
        if self.m_nCurOptMember == self.m_roomObj.GetMemberNum():
            self.m_nCurOptMember = 1
        else:
            self.m_nCurOptMember += 1

        return self.m_nCurOptMember

    def GetPrevPos(self, nPos):
        if nPos == 1:
            return self.m_roomObj.GetMemberNum()
        return nPos - 1

    def MoPai(self):
        pass

    def FaPai(self):
        self.m_nCurOptMember = self.GetPrevPos(self.m_roomObj.GetMemberPos(self.m_nZhuang))
        for _ in xrange(0, 3): # 轮数
            for _ in xrange(0, self.m_nMemberNum): # 人数
                nPos = self.GetNextPos()
                for i in xrange(0, 4): # 摸牌数
                    self.m_dictPosCarList[nPos].append()

    def StartJu(self):
        """
        开启新的一局
        :return:
        """
        if self.m_nCurJu > self.GetMaxJuNum():
            self.GameEnd()
            return

        self.m_nCurJu += 1
        self.DingZhuang()
        self.XiPai()


    def GameStart(self):
        pass

    def GameEnd(self):
        self.m_roomObj.OnGameEnd()
        self.m_roomObj = None

    def OnMemberExit(self, nMemberGID):
        pass

    def OnMemberEnter(self, nMemberGID):
        pass