# -*- coding: utf-8 -*-
# @Author  : jh.feng

import ff, ffext
import entity.entity_mgr as entity_mgr
import util.tick_mgr as tick_mgr
from util.enum_def import EStatusInRoom, RoomMemberProperty
import state.state_machine as state_machine
import state.room_state_waiting as room_state_waiting
import state.room_state_running as room_state_running

class RoomObj(object):
    def __init__(self, nRoomID, nMaster, roomMgr, gameRuleObj=None):
        self.m_nMaxMember = 4
        self.m_roomMgr = roomMgr
        self.m_szGameLogicScene = None
        self.m_nRoomID = nRoomID
        self.m_nMaster = nMaster
        self.m_gameRuleObj = gameRuleObj
        self.m_dictMember = {} # member -> [nPos, status]

        # 初始化状态机
        self.m_sm = state_machine.StateMachine()
        self.m_sm.ChangeState(room_state_waiting.RoomStateWaiting(self))

        self.MemberEnter(nMaster)

    def GetRoomID(self):
        return self.m_nRoomID

    def Serial(self):
        dictSerial = {
            "id": self.m_nRoomID,
            "member": self.m_dictMember.keys(),
            "master": self.m_nMaster,
        }
        return dictSerial

    def CanStartGame(self):
        if self.m_sm.IsInState(room_state_running.RoomStateRunning) is True:
            return False

        return len(self.m_dictMember) == self.m_nMaxMember

    def StartGameOnRoom(self):
        ffext.LOGINFO("FFSCENE_PYTHON", "StartGameOnRoom {0}".format(self.GetRoomID()))
        self.m_sm.ChangeState(room_state_running.RoomStateRunning(self))
        for nMember in self.m_dictMember.iterkeys():
            Player = entity_mgr.GetEntity(nMember)
            Player.SetRoomID(self.GetRoomID())
        # self.m_gameRuleObj.Start()
        tick_mgr.RegisterOnceTick(10 * 1000, self.m_roomMgr.OnGameEnd, self.GetRoomID())

    def MemberEnter(self, nMember):
        self.m_sm.GetCurState().MemberEnter(nMember)

    def MemberExit(self, nMember):
        self.m_sm.GetCurState().MemberExit(nMember)

    def MemberOffline(self, nMember):
        self.m_sm.GetCurState().MemberOffline(nMember)

    def Dismiss(self):
        self.m_roomMgr.OnRoomDismiss(self.GetRoomID(), self.m_dictMember.keys())
        self.Destroy()

    def Destroy(self):
        self.m_sm.Destroy()
        self.m_roomMgr = None

    def GetEmptyPos(self):
        return self.m_nMaxMember - len(self.m_dictMember)

    def GenPos(self):
        for nPos in xrange(1, self.m_nMaxMember + 1):
            bExist = False
            for dictData in self.m_dictMember.itervalues():
                nHavePos = dictData[RoomMemberProperty.ePos]
                if nHavePos == nPos:
                    bExist = True
                    break
            if bExist is False:
                return nPos
        assert False

