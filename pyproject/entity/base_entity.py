# -*- coding:utf-8 -*-

import util.tick_mgr as tick_mgr

g_nPersistentGap = 15 * 1000# 1000 * 60 * 5

class BaseEntity(object):
    def __init__(self):
        self.m_sceneObj = None
        self.m_listCompmentName = []
        self.m_nTick2Persistent = None
        self.StartOnceTick()

    def SetScene(self, sceneObj):
        self.m_sceneObj = sceneObj

    def GetScene(self):
        return self.m_sceneObj

    def StopOnceTick(self):
        if self.m_nTick2Persistent is None:
            return
        tick_mgr.UnRegisterOnceTick(self.m_nTick2Persistent)
        self.m_nTick2Persistent = None

    def StartOnceTick(self):
        self.StopOnceTick()
        self.m_nTick2Persistent = tick_mgr.RegisterOnceTick(g_nPersistentGap, self.OnTimerPersistent)

    def OnTimerPersistent(self):
        self.StartOnceTick()
        self.Persistent()

    def AddCompment(self, compObj):
        szCompName = compObj.GetName()
        self.m_listCompmentName.append(szCompName)
        setattr(self, szCompName, compObj)

    def Destroy(self):
        self.StopOnceTick()
        self.Persistent()

        for szOneCompment in self.m_listCompmentName:
            compObj = getattr(self, szOneCompment)
            compObj.Destroy()
        self.m_listCompmentName = None
        self.m_sceneObj = None
