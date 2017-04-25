# coding=UTF-8
import ffext
import sys, json
sys.path.append("./pyproject")

import rpc.rpc_def as rpc_def
import room_service.room_mgr as room_mgr
import db.dbs_client as dbs_client

import proto.login_pb2 as login_pb2
@ffext.session_call(rpc_def.Gac2RoomServiceCreateRoom, login_pb2.request_login)
def Gac2RoomServiceCreateRoom(session, reqObj):
    ffext.LOGINFO("FFSCENE_PYTHON", "Gac2RoomServiceCreateRoom {0}".format(session))
    room_mgr._roomMgr.CreateRoom(session, {})

@ffext.session_call(rpc_def.Gac2RoomServiceEnterRoom, login_pb2.request_login)
def Gac2RoomServiceEnterRoom(session, reqObj):
    room_mgr._roomMgr.EnterRoom(session)
    room_mgr._roomMgr.StartGame(session)

@ffext.reg_service(rpc_def.OnPlayerOffline)
def OnPlayerOffline(session):
    # ffext.LOGINFO("FFSCENE_PYTHON", "RoomCenter player offline {0}".format(session))
    session = session["0"]
    room_mgr.OnPlayerLeaveScene(session)
    return {"ret": True}

@ffext.reg_service(rpc_def.Logic2RoomServiceGameEnd)
def Logic2RoomServiceGameEnd(dictData):
    ffext.LOGINFO("FFSCENE_PYTHON", "Logic2RoomServiceGameEnd {0}".format(json.dumps(dictData)))
    from rpc.rpc_property_def import RpcProperty
    nRoomID = dictData[RpcProperty.ret]
    room_mgr.OnGameEnd(nRoomID)

