# -*- coding: utf-8 -*-
# @Author  : jh.feng
import ffext
import conf as conf
import rpc.rpc_def as rpc_def

class GateMgr(object):
    def __init__(self):
        self.m_dictGate2SessionNum = {}

    def GetGateName(self, i):
        return "gate@{0}".format(i)

    def GetMinestSessionGate(self):
        nGateNum = conf.dict_cfg["gate"]["num"]
        szGateDst = None
        nMinestNum = None
        for i in xrange(0, nGateNum):
            nNum = self.m_dictGate2SessionNum.get(self.GetGateName(i), 0)
            if nMinestNum is None or nMinestNum > nNum:
                nMinestNum = nNum
                szGateDst = self.GetGateName(i)

        assert szGateDst is not None
        return szGateDst

    def OnSessionOnline(self, szGate, session):
        if szGate not in self.m_dictGate2SessionNum:
            self.m_dictGate2SessionNum[szGate] = 0
        self.m_dictGate2SessionNum[szGate] += 1

    def OnSessionOffline(self, szGate, session):
        self.m_dictGate2SessionNum[szGate] -= 1

_gateMgr = GateMgr()

@ffext.reg_service(rpc_def.GetGateIp)
def GetMinestSessionGate(session):
    szGateName = _gateMgr.GetMinestSessionGate()
    szGateAddr = conf.dict_cfg["gate"][szGateName]
    return {"0": szGateAddr}

@ffext.reg_service(rpc_def.OnSessionConnectGate)
def OnSessionConnectGate(session, szGate):
    _gateMgr.OnSessionOnline(szGate, session)

@ffext.reg_service(rpc_def.OnSessionDisConnGate)
def OnSessionDisConnGate(session, szGate):
    _gateMgr.OnSessionOffline(szGate, session)