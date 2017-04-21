# -*- coding: utf-8 -*-
import db.table.table_property_def as table_property_def
import proto.login_pb2 as login_pb2

class MjPlayer(object):
    def __init__(self):
        super(MjPlayer, self).__init__()
        self.m_session = None
        self.m_szName = None
        self.m_nSex = 0
        self.ip         = None
        self.gate_name  = None

    def GetGlobalID(self):
        return self.m_session

    def InitFromDict(self, dictSserial):
        self.m_session = dictSserial[table_property_def.Player.SESSION_ID]
        self.m_szName = dictSserial[table_property_def.Player.NAME]
        self.m_nSex = dictSserial[table_property_def.Player.SEX]
        self.ip = dictSserial[table_property_def.Player.IP]
        self.gate_name = dictSserial[table_property_def.Player.GATE_NAME]

    def Serial2Client(self):
        syn_req = login_pb2.syn_player_data()
        syn_req.ret = 0
        syn_req.session = self.m_session
        syn_req.name = self.m_szName
        syn_req.sex = self.m_nSex
        syn_req.money_info = ""
        syn_req.bag_item_info = ""
        return syn_req.SerializeToString()
