# coding=UTF-8
import os
import time
import ffext
import event_bus

import sys
sys.path.append("./pyproject")

import json
import proto.recv_msg_pb2 as recv_msg_pb2
import rpc.scene_def as scene_def
import login.login_mgr as login_mgr

def OnEnterLoginScene(session, src, data):
    import proto.login_pb2 as login_pb2
    rsp_login = login_pb2.response_login()
    rsp_login.ret = 0
    rsp_login.session_id = int(session)
    import rpc.rpc_def as rpc_def
    ffext.send_msg_session(session, rpc_def.ResponseLogin, rsp_login.SerializeToString())

    loginPlayer = login_mgr.GetPlayer(session)
    assert loginPlayer is not None

    ffext.change_session_scene(session, scene_def.ROOM_SCENE, json.dumps(loginPlayer.Serial2Dict()))
    ffext.LOGINFO("FFSCENE", "Auth done, request change 2 room center {0}, {1}".format(session, json.dumps(loginPlayer.Serial2Dict())))

ffext.g_session_enter_callback = OnEnterLoginScene
