# -*- coding: utf-8 -*-
# @Author  : jh.feng

from util.enum_def import EGameRule
import gas.gas_mj.gas_mj_mgr as gas_mj_mgr

class GasGameRuleMgr(object):
    def __init__(self):

        self.m_dictID2GameRule = {
            EGameRule.eGameRuleMj: gas_mj_mgr.GasMjRule,
        }

    def GetGameRule(self, nRuleType):
        return self.m_dictID2GameRule[nRuleType]

_gameRuleMgr = GasGameRuleMgr()
GetGameRule = _gameRuleMgr.GetGameRule
