# -*- coding: utf-8 -*-

class RoomPlayer(object):
    def __init__(self):
        self.m_session = None
        self.m_szName = None
        self.m_nSex = 0
        self.m_GoldCoin = 0

    def GetSession(self):
        return self.m_session

    def InitFromDict(self, dictData):
        self.m_session = dictData["session"]
        self.m_szName = dictData["name"]
        self.m_nSex = dictData["sex"]

    def Serial2Client(self):
        pass