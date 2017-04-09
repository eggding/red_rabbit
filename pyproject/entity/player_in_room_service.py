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
        self.m_session = int(dictData["session"])
        self.m_szName = dictData["name"]
        self.m_nSex = int(dictData["sex"])

    def Serial2Client(self):
        import proto.login_pb2 as login_pb2
        syn_req = login_pb2.syn_player_data()
        syn_req.ret = 0
        syn_req.session = self.m_session
        syn_req.name = self.m_szName
        syn_req.sex = self.m_nSex
        syn_req.money_info = ""
        syn_req.bag_item_info = ""
        return syn_req.SerializeToString()