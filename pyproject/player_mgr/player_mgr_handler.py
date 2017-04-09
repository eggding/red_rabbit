# -*- coding: utf-8 -*-
from player_mgr_model import *
import ffext
import msg_def.ttypes as msg_def
from db import dbservice
import proto.login_pb2 as login_pb2

@ffext.session_verify_callback
def real_session_verify(szAuthKey, online_time, ip, gate_name):
    '''
    '''
    req_login = login_pb2.request_login()
    try:
        req_login.ParseFromString(szAuthKey)
    except:
        return []

    szAuthKey = req_login.auth_info
    session_id = dbservice.get_session_by_auth_key(szAuthKey)
    player = player_t(session_id)
    player.nick_name = session_id
    player.password  = session_id
    player.online_time = online_time
    player.ip          = ip
    player.gate_name   = gate_name
    ffext.singleton(player_mgr_t).add(player.id(), player)

    # print('real_session_verify用户名[%s]对应的id[%s]'%(player.nick_name, player.id()))
    # #异步载入数据库中的数据
    # def callback():
    #     print('real_session_verify载入数据库数据完成%s'%(player.nick_name))

    # dbservice.load_player(player, callback)
    return [str(player.id())]


@ffext.session_enter_callback
def real_session_enter(session_id, from_scene, extra_data):
    print("real_session_enter ", session_id, from_scene, extra_data)


@ffext.session_offline_callback
def real_session_offline(session_id, online_time):
    import rpc.scene_def as scene_def
    import rpc.rpc_def as rpc_def
    ffext.LOGINFO("FFSCENE", "real_session_offline {0}, last scene {1}".format(session_id, scene_def.CUR_SCENE_NAME))
    ffext.singleton(player_mgr_t).remove(session_id)

    def cb(err_, msg_):
        pass
    ffext.call_service(scene_def.ROOM_SCENE, rpc_def.OnPlayerOffline, {"0": session_id}, cb)




