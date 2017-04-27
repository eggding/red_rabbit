# -*- coding: utf-8 -*-
# @Author  : jh.feng

from util.enum_def import EGameRule
import entity.rule_base as rule_base

class GasMjRule(rule_base.GameRuleBase):
    def __init__(self, roomObj):
        super(GasMjRule, self).__init__(EGameRule.eGameRuleMj)

        self.m_roomObj = roomObj
        self.m_dictCfg = None

        # 场数
        self.m_nCurChang = 0

        # 局数
        self.m_nCurJu = 0

    def InitWithCfg(self, dictCfg):
        self.m_dictCfg = dictCfg

    def StartNewChang(self):
        """
        开启新的一场玩法
        :return:
        """
        if self.m_nCurChang > self.m_dictCfg["change_num"]:
            self.GameEnd()
            return

        self.m_nCurChang += 1


    def GameStart(self):
        pass

    def GameEnd(self):
        self.m_roomObj.OnGameEnd()
        self.m_roomObj = None

    def OnMemberExit(self, nMemberGID):
        pass

    def OnMemberEnter(self, nMemberGID):
        pass