import ffext
import sys
sys.path.append("./pyproject")

import db.dbservice as dbservice

import rpc.rpc_def as rpc_def
import room_service.room_mgr as room_mgr
import entity.player_in_room_service as player_in_room_service
import rpc.scene_def as scene_def

scene_def.CUR_SCENE_NAME = scene_def.ROOM_SCENE

def OnLoadPlayerDataDone(dictSerialData):
    roomPlayer = player_in_room_service.RoomPlayer()
    roomPlayer.InitFromDict(dictSerialData)
    room_mgr.OnPlayerEnterScene(roomPlayer)

    import json
    ffext.send_msg_session(roomPlayer.GetSession(), rpc_def.RoomService2GacSynPlayerData, json.dumps(dictSerialData))

def OnPlayerEnterScene(session, szSrcScene, dictSerialData):
    print("OnPlayerEnterScene ", session, szSrcScene, dictSerialData)
    if szSrcScene == scene_def.LOGIN_SCENE:
        dbservice.load_player(session, OnLoadPlayerDataDone)
    else:
        OnLoadPlayerDataDone(dictSerialData)

ffext.g_session_enter_callback = OnPlayerEnterScene

@ffext.session_call(rpc_def.Gac2RoomServiceCreateCreateRoom)
def Gac2RoomServiceCreateCreateRoom(session_id, msg):
    print("session_id, msg ", session_id, msg)
    # player = ffext.singleton(player_mgr_t).get(session_id)
    # ffext.send_msg_session(session_id, 2, "try 2 change scene...")
    # ffext.change_session_scene(session_id, "scene@1", "e")

@ffext.reg_service(rpc_def.OnPlayerOffline)
def OnPlayerOffline(session):
    session = session["0"]
    room_mgr.OnPlayerLeaveScene(session)
    return {"ret": True}