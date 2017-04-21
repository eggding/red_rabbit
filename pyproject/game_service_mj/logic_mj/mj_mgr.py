# -*- coding: utf-8 -*-
# @Author  : jh.feng
import ffext
import util.tick_mgr as tick_mgr
import entity.player_in_mj_service as player_in_mj_service
import entity.entity_mgr as entity_mgr

class RoomInMjService(object):
    def __init__(self):
        self.m_nRound = 0
        self.m_nCardNum = 100
        self.m_listMj = []
        self.m_dictMember = {}

    def Init(self):
        pass

    def StartGame(self):
        pass

class MjMgr(object):
    def __init__(self):
        pass


@ffext.session_enter_callback
def OnEnterScene(nPlayerGID, dictSerial):
    Player = player_in_mj_service.MjPlayer()
    Player.InitFromDict(dictSerial)
    entity_mgr.AddEntity(nPlayerGID, Player)

def OnLeaveScene(nPlayerGID):
    entity_mgr.DelEntity(nPlayerGID)
