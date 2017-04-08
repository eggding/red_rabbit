# coding=UTF-8

import entity.entity_mgr as entity_mgr

class RoomService(object):
    def __init__(self):
        self.m_dictRoomID2Room = {}
        self.m_dictSession2RoomID = {}

    def CreateRoom(self, session, data):
        pass

    def OnPlayerEnterScene(self, roomPlayer):
        entity_mgr.AddEntity(roomPlayer.GetSession(), roomPlayer)

    def OnPlayerLeaveScene(self, session):
        entity_mgr.DelEntity(session)


_room = RoomService()
OnPlayerEnterScene = _room.OnPlayerEnterScene
OnPlayerLeaveScene = _room.OnPlayerLeaveScene

