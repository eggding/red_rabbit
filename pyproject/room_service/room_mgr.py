# coding=UTF-8

import ff, ffext
import json
import entity.entity_mgr as entity_mgr
import rpc.rpc_def as rpc_def
import entity.player_in_room_service as player_in_room_service
import rpc.scene_def as scene_def
import db.dbs_client as dbs_client
import db.dbs_def as dbs_def
import util.util as util

class RoomService(object):
    def __init__(self):
        self.m_dictRoomID2Room = {}
        self.m_dictSession2RoomID = {}

    def CreateRoom(self, session, data):
        pass

    def OnPlayerEnterScene(self, roomPlayer):
        entity_mgr.AddEntity(roomPlayer.GetSession(), roomPlayer)

    def OnPlayerLeaveScene(self, session):
        Player = entity_mgr.GetEntity(session)
        if Player is not None:
            Player.Destroy()
        entity_mgr.DelEntity(session)

_roomMgr = RoomService()
OnPlayerLeaveScene = _roomMgr.OnPlayerLeaveScene


def OnLoadPlayerDataDone(dictSerialData, dictExtra):
    assert dictSerialData[dbs_def.FLAG] is True
    util.dict_merge(json.loads(dictExtra), dictSerialData)

    ffext.LOGINFO("FFSCENE_PYTHON", "OnLoadPlayerDataDone {0}".format(json.dumps(dictSerialData)))
    roomPlayer = player_in_room_service.RoomPlayer()
    roomPlayer.InitFromDict(dictSerialData)
    _roomMgr.OnPlayerEnterScene(roomPlayer)

    import proto.login_pb2 as login_pb2
    syn_scene = login_pb2.syn_enter_scene()
    syn_scene.ret = 0
    syn_scene.scene_id = 1
    syn_scene.scene_info = ff.service_name
    # ffext.send_msg_session(roomPlayer.GetSession(), rpc_def.SynSceneInfo, syn_scene.SerializeToString())
    # ffext.send_msg_session(roomPlayer.GetSession(), rpc_def.SynPlayerData, roomPlayer.Serial2Client())

def OnPlayerEnterScene(nPlayerGID, szSrcScene, dictSerialData):
    print("OnPlayerEnterScene room  ", nPlayerGID, dictSerialData)
    ffext.LOGINFO("FFSCENE_PYTHON", "enter room center {0}".format(nPlayerGID))
    if szSrcScene == scene_def.LOGIN_SCENE:
        print("start load player data from db")
        dbs_client.DoAsynCall(rpc_def.DbsLoadPlayerData, nPlayerGID, 0, nChannel=nPlayerGID, funCb=OnLoadPlayerDataDone, callbackParams=dictSerialData)
    else:
        OnLoadPlayerDataDone(dictSerialData, "{}")

ffext.g_session_enter_callback = OnPlayerEnterScene


