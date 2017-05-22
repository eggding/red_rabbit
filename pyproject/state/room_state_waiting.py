# -*- coding: utf-8 -*-
# @Author  : jh.feng

import ffext
import util.util as util
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
            dictState[RoomMemberProperty.eStatus] = EStatusInRoom.eUnReady
        else:
            roomObj.m_dictMember[nMember] = {
                RoomMemberProperty.ePos: roomObj.GenPos(),
                RoomMemberProperty.eStatus: EStatusInRoom.eUnReady
            }

        Player = entity_mgr.GetEntity(nMember)
        Player.SetRoomID(roomObj.GetRoomID())

        roomObj.SynGameInfo(nMember, bSynAll=True)
        roomObj.SynMemberState2All(nMember, EStatusInRoom.eUnReady)

        import json
        ffext.LOGINFO("FFSCENE_PYTHON", "RoomStateWaiting.MemberEnter {0} -> {1}".format(nMember, json.dumps(roomObj.m_dictMember)))
        return True

    def MemberReady(self, nMember):
        roomObj = self.GetOwner()
        if nMember not in roomObj.m_dictMember:
            return

        dictState = roomObj.m_dictMember[nMember]
        if EStatusInRoom.eReady == dictState[RoomMemberProperty.eStatus]:
            return

        dictState[RoomMemberProperty.eStatus] = EStatusInRoom.eReady
        roomObj.SynMemberState2All(nMember, EStatusInRoom.eReady)

        import json
        ffext.LOGINFO("FFSCENE_PYTHON", "RoomStateWaiting.MemberReady {0} -> {1}".format(nMember, json.dumps(roomObj.m_dictMember)))
        if roomObj.CanStartGame() is True:
            roomObj.StartGameOnRoom()

    def MemberExit(self, nMember):
        roomObj = self.GetOwner()
        Player = entity_mgr.GetEntity(nMember)
        Player.SetRoomID(None)

        assert nMember in roomObj.m_dictMember
        roomObj.SynMemberState2All(nMember, EStatusInRoom.eExitRoom)

        if 1 == len(roomObj.m_dictMember):
            roomObj.Dismiss()
        else:
            roomObj.m_dictMember.pop(nMember)

        # all is robot ?
        bAllIsRobot = True
        for nOneMember in roomObj.m_dictMember.iterkeys():
            if util.IsRobot(nOneMember) is False:
                bAllIsRobot = False
                break

        print("member exit all is robot ", bAllIsRobot)
        if bAllIsRobot is True and len(roomObj.m_dictMember) != 0:
            roomObj.Dismiss()

        import json
        ffext.LOGINFO("FFSCENE_PYTHON", "RoomStateWaiting.MemberExit {0} -> {1}".format(nMember, json.dumps(roomObj.m_dictMember)))

