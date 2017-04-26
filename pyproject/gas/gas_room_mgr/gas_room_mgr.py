# -*- coding: utf-8 -*-
# @Author  : jh.feng

import ff, ffext
import json
import entity.entity_mgr as entity_mgr
import rpc.rpc_def as rpc_def
import db.dbs_client as dbs_client
import db.dbs_def as dbs_def
import rpc.scene_def as scene_def
from rpc.rpc_property_def import RpcProperty

import gas_room_obj as gas_room_obj

class RoomService(object):
    def __init__(self):
        self.m_dictRoomID2Room = {}
        self.m_dictSession2RoomID = {}

    def OnRoomDismiss(self, nRoomID, listRoomPlayers):
        ffext.LOGINFO("FFSCENE_PYTHON", " GasRoomMgr.OnRoomDismiss {0}".format(nRoomID))
        self.m_dictRoomID2Room.pop(nRoomID)
        for nPlayerGID in listRoomPlayers:
            self.m_dictSession2RoomID.pop(nPlayerGID)

    def GetRoomObjByPlayerGID(self, nPlayerGID):
        nRoomID = self.m_dictSession2RoomID.get(nPlayerGID)
        if nRoomID is None:
            return None
        roomObj = self.m_dictRoomID2Room[nRoomID]
        return roomObj

    def EnterRoom(self, nPlayerGID, nRoomID=None):
        if nRoomID is None:
            ffext.call_service(scene_def.GCC_SCENE, rpc_def.Gas2GccGetRoomSceneByRoomID, {"room_id": 0,
                                                                                          "gas_id": ff.service_name,
                                                                                          "player_id": nPlayerGID})
            return

        roomObj = self.m_dictRoomID2Room.get(nRoomID)
        if roomObj is None:
            ffext.call_service(scene_def.GCC_SCENE, rpc_def.Gas2GccGetRoomSceneByRoomID, {"room_id": 0,
                                                                                          "gas_id": ff.service_name,
                                                                                          "player_id": nPlayerGID})
            return

        roomObj.MemberEnter(nPlayerGID)
        self.m_dictSession2RoomID[nPlayerGID] = nRoomID

    def OnGetRoomIDRet(self, nRoomID, nPlayerGID):
        ffext.LOGINFO("FFSCENE_PYTHON", " GasRoomMgr.OnGetRoomIDRet {0}, {1}".format(nRoomID, nPlayerGID))
        roomObj = gas_room_obj.RoomObj(nRoomID, nPlayerGID, self)
        self.m_dictRoomID2Room[nRoomID] = roomObj
        self.m_dictSession2RoomID[nPlayerGID] = nRoomID

    def CreateRoom(self, nRoomMaster):
        ffext.LOGINFO("FFSCENE_PYTHON", " GasRoomMgr.CreateRoom {0}".format(nRoomMaster))
        if nRoomMaster in self.m_dictSession2RoomID:
            return
        ffext.call_service(scene_def.GCC_SCENE, rpc_def.Gas2GccGenRoomID, {"player_id": nRoomMaster,
                                                                           "gas_id": ff.service_name})

    def ExitRoom(self, nPlayerGID):
        if nPlayerGID not in self.m_dictSession2RoomID:
            return

        self.m_dictSession2RoomID.pop(nPlayerGID)
        roomObj = self.GetRoomObjByPlayerGID(nPlayerGID)
        if roomObj is not None:
            roomObj.MemberExit(nPlayerGID)

    def OnGameEnd(self, nRoomId):
        roomObj = self.m_dictRoomID2Room[nRoomId]
        assert roomObj is not None
        roomObj.Dismiss()

    def OnEnterScene(self, roomPlayer):
        ffext.LOGINFO("FFSCENE_PYTHON", " OnEnterScene {0}".format(roomPlayer.GetGlobalID()))
        assert roomPlayer is not None

    def OnLeaveScene(self, nPlayerGID):
        ffext.LOGINFO("FFSCENE_PYTHON", "OnPlayerLeaveScene {0}".format(nPlayerGID))

        roomObj = self.GetRoomObjByPlayerGID(nPlayerGID)
        if roomObj is not None:
            roomObj.MemberExit(nPlayerGID)

    def OnMemberExit(self, nPlayerGID):
        roomObj = self.GetRoomObjByPlayerGID(nPlayerGID)
        if roomObj is None:
            return
        roomObj.MemberExit(nPlayerGID)

    def OnMemberEnter(self, nPlayerGID):
        roomObj = self.GetRoomObjByPlayerGID(nPlayerGID)
        if roomObj is None:
            return
        roomObj.OnMemberEnter(nPlayerGID)

_roomMgr = RoomService()
EnterRoom = _roomMgr.EnterRoom
OnMemberExit = _roomMgr.OnMemberExit
OnMemberEnter = _roomMgr.OnMemberEnter

@ffext.reg_service(rpc_def.Gcc2GasRetGetRoomScene)
def Gcc2GasRetGetRoomScene(dictData):
    szRoomGasID = dictData["gas_id"]
    nPlayerGID = dictData["player_id"]
    nRoomID = dictData["room_id"]
    if nRoomID == 0:
        return
    Player = entity_mgr.GetEntity(nPlayerGID)
    if Player is None:
        return

    if szRoomGasID != ff.service_name:
        Player.RequestChangeScene(szRoomGasID, {"room_id": nRoomID})
    else:
        _roomMgr.EnterRoom(nPlayerGID, nRoomID)

@ffext.reg_service(rpc_def.Gcc2GasRetGenRoomID)
def Gcc2GasRetGenRoomID(dictData):
    nRoomID = dictData["room_id"]
    nPlayerGID = dictData["player_id"]
    _roomMgr.OnGetRoomIDRet(nRoomID, nPlayerGID)

import proto.login_pb2 as login_pb2
@ffext.session_call(rpc_def.Gac2GasCreateRoom, login_pb2.request_login)
def Gac2GasCreateRoom(nPlayerGID, reqObj):
    _roomMgr.CreateRoom(nPlayerGID)

@ffext.session_call(rpc_def.Gac2GasEnterRoom, login_pb2.request_login)
def Gac2GasEnterRoom(nPlayerGID, reqObj):
    _roomMgr.EnterRoom(nPlayerGID)
