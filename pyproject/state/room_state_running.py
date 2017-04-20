# -*- coding: utf-8 -*-
# @Author  : jh.feng

import state_machine as state_machine
from util.enum_def import EStatusInRoom, RoomMemberProperty

class RoomStateRunning(state_machine.StateBase):
    def __init__(self, owner):
        super(RoomStateRunning, self).__init__(owner)

    def MemberEnter(self, nMember):
        roomObj = self.GetOwner()
        if nMember not in roomObj.m_dictMember:
            return

        dictState = roomObj.m_dictMember[nMember]
        dictState[RoomMemberProperty.eStatus] = EStatusInRoom.ePlaying

    def MemberExit(self, nMember):
        self.MemberOffline(nMember)

    def MemberOffline(self, nMember):
        roomObj = self.GetOwner()
        assert nMember in roomObj.m_dictMember
        dictState = roomObj.m_dictMember[nMember]
        dictState[RoomMemberProperty.eStatus] = EStatusInRoom.eOffline
