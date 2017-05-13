# -*- coding: utf-8 -*-
# @Author  : jh.feng

import ffext
import time
import rpc.rpc_def as rpc_def
import rpc.scene_def as scene_def
import conf as conf
import util.tick_mgr as tick_mgr

class GameManager(object):
    def __init__(self):
        self.m_bNoticeAllService = False
        self.m_nPeerGap = 30
        self.m_dictAllService = {
            scene_def.GCC_SCENE: False,
            scene_def.LOGIN_SCENE: False,
            scene_def.DB_SERVICE_DEFAULT: False,
        }

        nGasNum = conf.dict_cfg["gas"]["num"]
        for i in xrange(0, nGasNum):
            self.m_dictAllService["gas@{0}".format(i)] = None

        nDbQueueNum = conf.dict_cfg["dbs"]["queue_num"]
        for i in xrange(0, nDbQueueNum):
            self.m_dictAllService["{0}{1}".format(scene_def.DB_SERVICE_DEFAULT, i)] = None

    def Peer(self):
        tick_mgr.RegisterOnceTick(self.m_nPeerGap * 1000,  self.Peer)
        for szService in self.m_dictAllService.iterkeys():
            ffext.call_service(szService, rpc_def.Peer, {})

    def OnRspPeer(self, szService):
        self.m_dictAllService[szService] = int(time.time())

    def CheckServiceDisConn(self):
        tick_mgr.RegisterOnceTick(5000, self.Peer)
        for szService, nUpdTime in self.m_dictAllService.iteritems():
            nGap = time.time() - nUpdTime
            if nGap > 2 * self.m_nPeerGap:
                self.OnServiceDisConn(szService)

    def CheckAllServiceDone(self):
        for szService, nHeartBeatTime in self.m_dictAllService.iteritems():
            if nHeartBeatTime is None:
                return
        self.NoticeAll()
        self.CheckServiceDisConn()

    def NoticeAll(self):
        for szService in self.m_dictAllService.iterkeys():
            ffext.call_service(szService, rpc_def.OnAllServiceStartUp, {})

        tick_mgr.RegisterOnceTick(5000, self.Peer)

    def OnServiceDisConn(self, szServiceName):
        self.m_dictAllService[szServiceName] = False

    def OnServiceConn(self, szServiceName):
        self.m_dictAllService[szServiceName] = True
        self.CheckAllServiceDone()

_gamMgr = GameManager()

@ffext.reg_service(rpc_def.OnServiceConn)
def OnServiceConn(dictSerial):
    szService = dictSerial["service"]
    ffext.LOGINFO("FFSCENE_PYTHON", "GameMgr.OnServiceConn {0}".format(szService))
    _gamMgr.OnServiceConn(szService)

@ffext.reg_service(rpc_def.RspPeer)
def RspPeer(dictData):
    szService = dictData["service"]
    _gamMgr.OnRspPeer(szService)
