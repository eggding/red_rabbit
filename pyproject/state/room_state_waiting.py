# -*- coding: utf-8 -*-
# @Author  : jh.feng

import ffext
import entity.entity_mgr as entity_mgr
import state_machine as state_machine
from util.enum_def import EStatusInRoom, RoomMemberProperty, EMemberEvent

class RoomStateWaiting(state_machine.StateBase):
    def __init__(self, owner):
        super(RoomStateWaiting, self).__init__(owner)

    def MemberEnter(self, nMember):
        roomObj = self.GetOwner()
        if len(roomObj.m_dictMember) >= roomObj.m_nMaxMember:
            return False

        if nMember in roomObj.m_dictMember:
            dictState = roomObj.m_dictMember[nMember]
            dictState[RoomMemberProperty.eStatus] = EStatusInRoom.eReady
        else:
            roomObj.m_dictMember[nMember] = {
                RoomMemberProperty.ePos: roomObj.GenPos(),
                RoomMemberProperty.eStatus: EStatusInRoom.eReady
            }

        Player = entity_mgr.GetEntity(nMember)
        Player.SetRoomID(roomObj.GetRoomID())

        roomObj.SynGameInfo(nMember, bSynAll=True)
        roomObj.NoticeMemberEvent(EMemberEvent.evMemberEnter, nMember)

        import json
        ffext.LOGINFO("FFSCENE_PYTHON", "RoomStateWaiting.MemberEnter {0} -> {1}".format(nMember, json.dumps(roomObj.m_dictMember)))

        if roomObj.CanStartGame() is True:
            roomObj.StartGameOnRoom()

        return True

    def MemberExit(self, nMember):
        roomObj = self.GetOwner()
        Player = entity_mgr.GetEntity(nMember)
        Player.SetRoomID(None)

        roomObj.NoticeMemberEvent(EMemberEvent.evMemberExit, nMember)

        assert nMember in roomObj.m_dictMember
        if 1 == len(roomObj.m_dictMember):
            roomObj.Dismiss()
        else:
            roomObj.m_dictMember.pop(nMember)

        import json
        ffext.LOGINFO("FFSCENE_PYTHON", "RoomStateWaiting.MemberExit {0} -> {1}".format(nMember, json.dumps(roomObj.m_dictMember)))

