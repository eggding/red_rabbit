# -*- coding: utf-8 -*-
# @Author  : jh.feng

import ffext
import json
import rpc.rpc_def as rpc_def
import entity.entity_mgr as entity_mgr
import state_machine as state_machine
from util.enum_def import EStatusInRoom, RoomMemberProperty, EMemberEvent

class RoomStateRunning(state_machine.StateBase):
    def __init__(self, owner):
        super(RoomStateRunning, self).__init__(owner)

    def MemberEnter(self, nMember):
        ffext.LOGINFO("FFSCENE_PYTHON", "RoomStateRunning.MemberEnter {0}".format(nMember))
        roomObj = self.GetOwner()
        if nMember not in roomObj.m_dictMember:
            return False

        Player = entity_mgr.GetEntity(nMember)
        Player.SetRoomID(roomObj.GetRoomID())

        dictState = roomObj.m_dictMember[nMember]
        dictState[RoomMemberProperty.eStatus] = EStatusInRoom.ePlaying

        roomObj.GetGameRule().OnMemberEnter(nMember)
        roomObj.SynGameInfo(nMember, bSynAll=True)
        roomObj.NoticeMemberEvent(EMemberEvent.evMemberEnter, nMember)
        return True

    def MemberExit(self, nMember):
        self.MemberOffline(nMember)

    def MemberOffline(self, nMember):
        ffext.LOGINFO("FFSCENE_PYTHON", "RoomStateRunning.MemberOffline {0}".format(nMember))
        roomObj = self.GetOwner()
        assert nMember in roomObj.m_dictMember
        dictState = roomObj.m_dictMember[nMember]
        dictState[RoomMemberProperty.eStatus] = EStatusInRoom.eOffline

        roomObj.GetGameRule().OnMemberExit(nMember)
        roomObj.NoticeMemberEvent(EMemberEvent.evMemberExit, nMember)

