# coding=UTF-8
import ffext
import sys, json
sys.path.append("./pyproject")

import db.dbservice as dbservice

import rpc.rpc_def as rpc_def
import room_service.room_mgr as room_mgr
import entity.player_in_room_service as player_in_room_service
import rpc.scene_def as scene_def
import db.dbs_client as dbs_client
import db.dbs_def as dbs_def

scene_def.CUR_SCENE_NAME = scene_def.ROOM_SCENE

def OnTimer(data):
    print("on timer.", data)
    ffext.once_timer(1500, OnTimer, data)

def OnLoadPlayerDataDone(dictSerialData):
    assert dictSerialData[dbs_def.FLAG] is True

    ffext.LOGINFO("FFSCENE_PYTHON", "OnLoadPlayerDataDone {0}".format(json.dumps(dictSerialData)))
    roomPlayer = player_in_room_service.RoomPlayer()
    roomPlayer.InitFromDict(dictSerialData)
    room_mgr.OnPlayerEnterScene(roomPlayer)

    import proto.login_pb2 as login_pb2
    syn_scene = login_pb2.syn_enter_scene()
    syn_scene.ret = 0
    syn_scene.scene_id = 1
    syn_scene.scene_info = scene_def.CUR_SCENE_NAME
    ffext.send_msg_session(roomPlayer.GetSession(), rpc_def.SynSceneInfo, syn_scene.SerializeToString())
    ffext.send_msg_session(roomPlayer.GetSession(), rpc_def.SynPlayerData, roomPlayer.Serial2Client())

def OnPlayerEnterScene(session, szSrcScene, dictSerialData):
    ffext.LOGINFO("FFSCENE_PYTHON", "enter room center {0}".format(session))
    if szSrcScene == scene_def.LOGIN_SCENE:
        dbs_client.DoAsynCall(rpc_def.DbsLoadPlayerData, session, funCb=OnLoadPlayerDataDone)
    else:
        OnLoadPlayerDataDone(dictSerialData)

ffext.g_session_enter_callback = OnPlayerEnterScene

# import proto.login_pb2 as login_pb2
# @ffext.session_call(rpc_def.Gac2RoomServiceGetEcho, login_pb2.request_login)
# def Gac2RoomServiceGetEcho(session_id, msg):
#     print("Gac2RoomServiceGetEcho, msg ", session_id, msg.auth_info)
#     rsp_login = login_pb2.response_login()
#     rsp_login.ret = 0
#     rsp_login.session_id = "get msg {0}".format(msg.auth_info)
#     ffext.send_msg_session(session_id, 30004, rsp_login.SerializeToString())
#
# @ffext.session_call(rpc_def.Gac2RoomServiceCreateCreateRoom)
# def Gac2RoomServiceCreateCreateRoom(session_id, msg):
#     print("session_id, msg ", session_id, msg)
#     # player = ffext.singleton(player_mgr_t).get(session_id)
#     # ffext.send_msg_session(session_id, 2, "try 2 change scene...")
#     # ffext.change_session_scene(session_id, "scene@1", "e")

@ffext.reg_service(rpc_def.OnPlayerOffline)
def OnPlayerOffline(session):
    ffext.LOGINFO("FFSCENE", "RoomCenter 玩家下线处理 {0}".format(session))
    session = session["0"]
    room_mgr.OnPlayerLeaveScene(session)
    return {"ret": True}