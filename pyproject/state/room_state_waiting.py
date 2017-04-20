# -*- coding: utf-8 -*-
# @Author  : jh.feng

import state_machine as state_machine
from util.enum_def import EStatusInRoom, RoomMemberProperty

class RoomStateWaiting(state_machine.StateBase):
    def __init__(self, owner):
        super(RoomStateWaiting, self).__init__(owner)

    def MemberEnter(self, nMember):
        roomObj = self.GetOwner()
        if len(roomObj.m_dictMember) >= roomObj.m_nMaxMember:
            return

        if nMember in roomObj.m_dictMember:
            dictState = roomObj.m_dictMember[nMember]
            dictState[RoomMemberProperty.eStatus] = EStatusInRoom.eReady
        else:
            roomObj.m_dictMember[nMember] = {
                RoomMemberProperty.ePos: roomObj.GenPos(),
                RoomMemberProperty.eStatus: EStatusInRoom.eReady
            }

    def MemberExit(self, nMember):
        roomObj = self.GetOwner()
        assert nMember in roomObj.m_dictMember
        roomObj.m_dictMember.pop(nMember)

    def MemberOffline(self, nMember):
        roomObj = self.GetOwner()
        assert nMember in roomObj.m_dictMember
        dictState = roomObj.m_dictMember[nMember]
        dictState[RoomMemberProperty.eStatus] = EStatusInRoom.eOffline
