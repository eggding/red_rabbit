# -*- coding: utf-8 -*-
# @Author  : jh.feng

class GccRoomObj(object):
    def __init__(self):
        self.m_GasID = None
        self.m_bIsRunning = False
        self.m_dictRoomMember = None

    def SetIsRunning(self):
        self.m_bIsRunning = True

    def IsRunning(self):
        return self.m_bIsRunning

    def SetGasID(self, szGasID):
        self.m_GasID = szGasID

    def GetGasID(self):
        return self.m_GasID

    def Init(self, dictData):
        pass