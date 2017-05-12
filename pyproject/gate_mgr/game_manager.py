# -*- coding: utf-8 -*-
# @Author  : jh.feng

import ffext
import rpc.rpc_def as rpc_def
import rpc.scene_def as scene_def
import conf as conf

class GameManager(object):
    def __init__(self):
        self.m_bNoticeAllService = False
        self.m_dictAllService = {
            scene_def.GCC_SCENE: False,
            scene_def.LOGIN_SCENE: False,
            scene_def.DB_SERVICE_DEFAULT: False,
        }

        nGasNum = conf.dict_cfg["gas"]["num"]
        for i in xrange(0, nGasNum):
            self.m_dictAllService["gas@{0}".format(i)] = False

        nDbQueueNum = conf.dict_cfg["dbs"]["queue_num"]
        for i in xrange(0, nDbQueueNum):
            self.m_dictAllService["{0}{1}".format(scene_def.DB_SERVICE_DEFAULT, i)] = False

    def CheckAllServiceDone(self):
        for szService, bFlag in self.m_dictAllService.iteritems():
            if bFlag is False:
                return
        self.NoticeAll()

    def NoticeAll(self):
        for szService in self.m_dictAllService.iterkeys():
            ffext.call_service(szService, rpc_def.OnAllServiceStartUp, {})

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
