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

    def GetGlobalID(self):
        return self.m_session

    def InitFromDict(self, session, dictSserial):
        self.m_session = session
        self.m_szName = dictSserial[table_property_def.Player.NAME]
        self.m_nSex = dictSserial[table_property_def.Player.SEX]
        self.ip = dictSserial[table_property_def.Player.IP]
