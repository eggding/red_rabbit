# -*- coding: utf-8 -*-
# @Author  : jh.feng
import ff
import ffext
import util.tick_mgr as tick_mgr

RESIDUAL_TIME = 10 * 60 * 1000

class ResidualMgr(object):
    def __init__(self, sceneObj):
        self.m_sceneObj = sceneObj
        self.m_dictRsidualPlayer = {} # nplayerid -> tickid

    def IsPlayerInResidual(self, nPlayerGID):
        return True if nPlayerGID in self.m_dictRsidualPlayer else False

    def OnResdualTimeOut(self, nPlayerGID):
        ffext.LOGINFO("FFSCENE_PYTHON", "OnResdualTimeOut {0}, {1}".format(nPlayerGID, ff.service_name))
        self.m_dictRsidualPlayer.pop(nPlayerGID)
        self.m_sceneObj.PlayerTrueOffline(nPlayerGID)

    def RemoveResidualPlayer(self, nPlayerGID):
        assert nPlayerGID in self.m_dictRsidualPlayer
        tick_mgr.UnRegisterOnceTick(self.m_dictRsidualPlayer[nPlayerGID])
        self.m_dictRsidualPlayer.pop(nPlayerGID)
        ffext.LOGINFO("FFSCENE_PYTHON", "RemoveResidualPlayer {0}".format(nPlayerGID))

    def AddResidualPlayer(self, nPlayerGID):
        assert nPlayerGID not in self.m_dictRsidualPlayer
        nTickID = tick_mgr.RegisterOnceTick(RESIDUAL_TIME, self.OnResdualTimeOut, nPlayerGID)
        self.m_dictRsidualPlayer[nPlayerGID] = nTickID
        ffext.LOGINFO("FFSCENE_PYTHON", "AddResidualPlayer {0}".format(nPlayerGID))