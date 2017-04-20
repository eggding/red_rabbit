# -*- coding: utf-8 -*-
# @Author  : jh.feng
import util.tick_mgr as tick_mgr

RESIDUAL_TIME = 10 * 60 * 1000

class ResidualMgr(object):
    def __init__(self, sceneObj):
        self.m_sceneObj = sceneObj
        self.m_dictRsidualPlayer = {} # nplayerid -> tickid

    def OnResdualTimeOut(self, nPlayerGID):
        self.m_dictRsidualPlayer.pop(nPlayerGID)
        self.m_sceneObj.OnPlayerLeaveScene()

    def RemoveResidualPlayer(self, nPlayerGID):
        assert nPlayerGID in self.m_dictRsidualPlayer
        self.OnResdualTimeOut(nPlayerGID)

    def AddResidualPlayer(self, nPlayerGID):
        assert nPlayerGID not in self.m_dictRsidualPlayer
        nTickID = tick_mgr.RegisterOnceTick(RESIDUAL_TIME, self.OnResdualTimeOut, nPlayerGID)
        self.m_dictRsidualPlayer[nPlayerGID] = nTickID