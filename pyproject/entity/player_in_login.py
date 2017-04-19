# -*- coding: utf-8 -*-
import db.table.table_property_def as table_property_def

class PlayerInLogin(object):
    def __init__(self, session_id_, online_time=0, ip=None, gate=None):
        self.session_id = session_id_
        self.online_time = online_time
        self.ip = ip
        self.gate = gate

    def Serial2Dict(self):
        dictSerial = {
            table_property_def.Player.IP: self.ip,
            table_property_def.Player.GATE_NAME: self.gate,
        }
        return dictSerial

    def GetGlobalID(self):
        return self.session_id
