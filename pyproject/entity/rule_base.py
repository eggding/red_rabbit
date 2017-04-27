# -*- coding: utf-8 -*-
# @Author  : jh.feng

class GameRuleBase(object):
    def __init__(self, nRuleType):
        self.m_nRuleType = nRuleType

    def OnMemberExit(self, nMemberGID):
        assert False

    def OnMemberEnter(self, nMemberGID):
        assert False