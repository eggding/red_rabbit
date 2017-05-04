# -*- coding: utf-8 -*-
# @Author  : jh.feng

import ff, ffext
import entity.entity_mgr as entity_mgr
import rpc.rpc_def as rpc_def
import rpc.scene_def as scene_def
import proto.query_room_scene_pb2 as query_room_scene_pb2
import gas_room_obj as gas_room_obj
import cfg_py.parameter_common as parameter_common

from util.enum_def import EMoneyType

class RoomService(object):
    def __init__(self):
        self.m_dictRoomID2Room = {}

    def GetCreateRoomNeedMoney(self):
        return parameter_common.parameter_common[3]["参数"]

    def OnRoomDismiss(self, nRoomID, listRoomPlayers):
        ffext.LOGINFO("FFSCENE_PYTHON", " GasRoomMgr.OnRoomDismiss {0}".format(nRoomID))
        self.m_dictRoomID2Room.pop(nRoomID)
        for nPlayerGID in listRoomPlayers:
            Player = entity_mgr.GetEntity(nPlayerGID)
            assert Player is not None
            Player.SetRoomID(None)
            Player.GetScene().OnPlayerGameEnd(nPlayerGID)

        ffext.call_service(scene_def.GCC_SCENE, rpc_def.Gas2GccOnRoomDismiss, {"room_id": nRoomID})

    def GetRoomObjByPlayerGID(self, nPlayerGID):
        Player = entity_mgr.GetEntity(nPlayerGID)
        nRoomID = Player.GetRoomID()
        if nRoomID is None:
            return None
        roomObj = self.m_dictRoomID2Room[nRoomID]
        return roomObj

    def EnterRoom(self, nPlayerGID, nRoomID=None):
        if nRoomID is None:
            return

        if 0 == nRoomID and len(self.m_dictRoomID2Room) != 0:
            nRoomID = self.m_dictRoomID2Room.keys()[0]

        roomObj = self.m_dictRoomID2Room.get(nRoomID)
        if roomObj is None:
            return
        roomObj.MemberEnter(nPlayerGID)

    def OnGetRoomIDRet(self, nRoomID, nPlayerGID, dictCfg):
        ffext.LOGINFO("FFSCENE_PYTHON", " GasRoomMgr.OnGetRoomIDRet {0}, {1}".format(nRoomID, nPlayerGID))
        roomObj = gas_room_obj.RoomObj(nRoomID, nPlayerGID, self, dictCfg)
        self.m_dictRoomID2Room[nRoomID] = roomObj

    def CreateRoom(self, nRoomMaster, dictRoomCfg):
        Player = entity_mgr.GetEntity(nRoomMaster)
        if Player.GetRoomID() is not None:
            return

        nNeedZhuanShiNum = self.GetCreateRoomNeedMoney()
        bIsAvg = True if dictRoomCfg.get('avg', 0) == 1 else False
        if bIsAvg is True:
            nDelZhuanShiNum = nNeedZhuanShiNum / dictRoomCfg.get("member_num", 4)
        else:
            nDelZhuanShiNum = nNeedZhuanShiNum

        if Player.IsMoneyEnough(EMoneyType.eZhuanShi, nDelZhuanShiNum) is False:
            return

        ffext.LOGINFO("FFSCENE_PYTHON", " GasRoomMgr.CreateRoom {0}".format(nRoomMaster))
        ffext.call_service(scene_def.GCC_SCENE, rpc_def.Gas2GccGenRoomID, {"player_id": nRoomMaster,
                                                                           "gas_id": ff.service_name,
                                                                           "cfg": dictRoomCfg})

    def ExitRoom(self, nPlayerGID):
        roomObj = self.GetRoomObjByPlayerGID(nPlayerGID)
        if roomObj is not None:
            roomObj.MemberExit(nPlayerGID)

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
        roomObj.MemberEnter(nPlayerGID)

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

    rsp = query_room_scene_pb2.query_room_scene_rsp()
    rsp.ret = 0
    rsp.room_id = nRoomID
    rsp.scene_name = szRoomGasID.encode('utf-8')
    ffext.send_msg_session(nPlayerGID, rpc_def.Gas2GacretQueryRoomScene, rsp.SerializeToString())

@ffext.reg_service(rpc_def.Gcc2GasRetGenRoomID)
def Gcc2GasRetGenRoomID(dictData):
    nRoomID = dictData["room_id"]
    nPlayerGID = dictData["player_id"]
    dictCfg = dictData["cfg"]
    _roomMgr.OnGetRoomIDRet(nRoomID, nPlayerGID, dictCfg)

@ffext.session_call(rpc_def.Gac2GasQueryRoomScene, query_room_scene_pb2.query_room_scene_req)
def Gac2GasQueryRoomScene(nPlayerGID, reqObj):
    nRoomID = reqObj.room_id
    ffext.call_service(scene_def.GCC_SCENE, rpc_def.Gas2GccGetRoomSceneByRoomID, {"room_id": nRoomID,
                                                                              "gas_id": ff.service_name,
                                                                              "player_id": nPlayerGID})

import proto.create_room_pb2 as create_room_pb2
@ffext.session_call(rpc_def.Gac2GasCreateRoom, create_room_pb2.create_room_req)
def GacGasCreateRoom(nPlayerGID, reqObj):
    # nGameType = reqObj.game_type
    gameCfg = reqObj.cfg
    dictRoomCfg = {
        "member_num": gameCfg.member_num,
        "multi": gameCfg.multi,
        "total_start_game_num": gameCfg.total_start_game_num,
        "opt": gameCfg.opt,
        "avg": 0,
    }
    _roomMgr.CreateRoom(nPlayerGID, dictRoomCfg)

import proto.enter_room_pb2 as enter_room_pb2
@ffext.session_call(rpc_def.Gac2GasEnterRoom, enter_room_pb2.enter_room_req)
def Gac2GasEnterRoom(nPlayerGID, reqObj):
    nRoomID = reqObj.room_id
    _roomMgr.EnterRoom(nPlayerGID, nRoomID)

import proto.opt_pb2 as opt_pb2
@ffext.session_call(rpc_def.Gac2GasOptMj, opt_pb2.opt_req)
def Gac2GasOptMj(nPlayerGID, reqObj):
    roomObj = _roomMgr.GetRoomObjByPlayerGID(nPlayerGID)
    if roomObj is None:
        return
    roomObj.GameRuleOpt(nPlayerGID, reqObj)
