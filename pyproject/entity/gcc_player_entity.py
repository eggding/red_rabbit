# -*- coding: utf-8 -*-
# @Author  : jh.feng

class GccPlayerEntity(object):
    def __init__(self):
        self.m_nPlayerGID = None
        self.m_szGasID = None
        self.m_szIp = None
        self.m_szGateName = None
        self.m_nState = None

    def GetState(self):
        return self.m_nState

    def SetState(self, nState):
        self.m_nState = nState

    def Destroy(self):
        pass

    def SetIp(self, szIp):
        self.m_szIp = szIp

    def SetGateName(self, szGateName):
        self.m_szGateName = szGateName

    def SetGasID(self, szGasID):
        self.m_szGasID = szGasID

    def GetGasID(self):
        return self.m_szGasID