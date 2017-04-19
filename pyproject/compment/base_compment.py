# -*- coding:utf-8 -*-

class BaseCompment(object):
    def __init__(self, owner, szName):
        self.m_szCompName = szName
        self.m_owner = owner

    def GetOwner(self):
        return self.m_owner

    def Destroy(self):
        self.m_owner = None
        self.OnDestroy()

    def GetName(self):
        return self.m_szCompName
