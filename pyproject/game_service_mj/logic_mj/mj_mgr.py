# -*- coding: utf-8 -*-
# @Author  : jh.feng
import ffext
import rpc.scene_def as scene_def
import rpc.rpc_def as rpc_def
from rpc.rpc_property_def import RpcProperty
import util.tick_mgr as tick_mgr
import entity.player_in_mj_service as player_in_mj_service
import entity.entity_mgr as entity_mgr
from util.enum_def import EStatusInRoom, RoomMemberProperty

class RoomInMjService(object):
    def __init__(self):
        self.m_bIsRunning = False
        self.m_nMaxMemberNum = 4
        self.m_nRoomID = 0
        self.m_nRound = 0
        self.m_nTurn = 0
        self.m_nJuShu = 0
        self.m_nCardNum = 100
        self.m_listMj = []
        self.m_dictMember = {}

    def Init(self, dictCfg):
        self.m_nRoomID = dictCfg["id"]
        self.m_dictMember = {}
        for nPlayerGID in dictCfg["member"]:
            self.m_dictMember[nPlayerGID] = EStatusInRoom.eUnReady

    def CanStartGame(self):
        for nStatus in self.m_dictMember.itervalues():
            if nStatus != EStatusInRoom.eReady:
                return False
        return True

    def StartGame(self):
        self.m_bIsRunning = True
        tick_mgr.RegisterOnceTick(30000, _mjMgr.OnGameOver, self.m_nRoomID)

    def GetAllMember(self):
        return self.m_dictMember.keys()

    def MemberExit(self, nPlayerGID):
        self.m_dictMember[nPlayerGID] = EStatusInRoom.eOffline

        # syn all

    def MemberEnter(self, nPlayerGID):
        if self.m_bIsRunning is True:
            self.m_dictMember[nPlayerGID] = EStatusInRoom.ePlaying
        else:
            self.m_dictMember[nPlayerGID] = EStatusInRoom.eReady
            if self.CanStartGame() is False:
                return
            for nGid in self.m_dictMember.iterkeys():
                self.m_dictMember[nGid] = EStatusInRoom.ePlaying
            self.StartGame()

class MjMgr(object):
    def __init__(self):
        self.m_dictRoomID2Room = {}
        self.m_dictSession2RoomID = {}

    def CreateMjRoomService(self, dictRoomData):
        nRoomID = dictRoomData["id"]
        roomObj = RoomInMjService()
        roomObj.Init(dictRoomData)
        self.m_dictRoomID2Room[nRoomID] = roomObj

    def OnGameOver(self, nRoomID):
        ffext.LOGINFO("FFSCENE_PYTHON", "MjService.OnGameOver {0} ".format(nRoomID))
        roomObj = self.m_dictRoomID2Room[nRoomID]

        listRoomMembers = roomObj.GetAllMember()
        for nPlayerGID in listRoomMembers:
            ffext.change_session_scene(nPlayerGID, scene_def.ROOM_SCENE, "")

        for nPlayerGID in listRoomMembers:
            self.m_dictSession2RoomID.pop(nPlayerGID)
            entity_mgr.DelEntity(nPlayerGID)
        self.m_dictRoomID2Room.pop(nRoomID)

        ffext.call_service(scene_def.ROOM_SCENE, rpc_def.Logic2RoomServiceGameEnd, {RpcProperty.ret: nRoomID})

    def OnPlayerEnterScene(self, nPlayerGID, nRoomID):
        ffext.LOGINFO("FFSCENE_PYTHON", "MjService.OnPlayerEnterScene {0}, {1}".format(nPlayerGID, nRoomID))
        roomObj = self.m_dictRoomID2Room[nRoomID]
        self.m_dictSession2RoomID[nPlayerGID] = nRoomID
        roomObj.MemberEnter(nPlayerGID)

    def OnPlayerLeaveScene(self, nPlayerGID):
        ffext.LOGINFO("FFSCENE_PYTHON", "MjService.OnPlayerLeaveScene {0}".format(nPlayerGID))
        nRoomID = self.m_dictSession2RoomID[nPlayerGID]
        roomObj = self.m_dictRoomID2Room[nRoomID]
        roomObj.MemberExit(nPlayerGID)

_mjMgr = MjMgr()
CreateMjRoomService = _mjMgr.CreateMjRoomService

@ffext.session_enter_callback
def OnEnterScene(nPlayerGID, szFromScene, dictSerial):
    ffext.LOGINFO("FFSCENE_PYTHON", "from {0} -> {1}, {2} enter mj scene".format(szFromScene, nPlayerGID, dictSerial))

    import json
    dictSerial = json.loads(dictSerial)
    if entity_mgr.GetEntity(nPlayerGID) is None:
        Player = player_in_mj_service.MjPlayer()
        Player.InitFromDict(nPlayerGID, dictSerial)
        entity_mgr.AddEntity(nPlayerGID, Player)

    nRoomID = dictSerial["room_id"]
    _mjMgr.OnPlayerEnterScene(nPlayerGID, nRoomID)

def OnLeaveScene(nPlayerGID):
    ffext.LOGINFO("FFSCENE_PYTHON", "{0} leave mj scene".format(nPlayerGID))
    _mjMgr.OnPlayerLeaveScene(nPlayerGID)
