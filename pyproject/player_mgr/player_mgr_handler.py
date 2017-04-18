# -*- coding: utf-8 -*-
from player_mgr_model import *
import ffext
import proto.login_pb2 as login_pb2
import db.dbs_client as dbs_client
import rpc.rpc_def as rpc_def
import db.dbs_def as dbs_def

def OnCreateUserSessionCb(dictRet, listBindData):
    print("OnCreateUserSessionCb")
    online_time, ip, gate_name, cb_id = listBindData
    nFlag = dictRet[dbs_def.FLAG]
    if nFlag is True:
        pass
    else:
        ffext.on_verify_auth_callback(0, "", cb_id)
        return

    if dictRet[dbs_def.SESSION] == 0:
        # no session
        ffext.on_verify_auth_callback(0, "", cb_id)
        return

    # {u'cb': 1, u'c': [u'SESSION_ID'], u'r': [[u'65601537']], u's': 0, u'f': True}
    session_id = int(dictRet[dbs_def.SESSION])
    player = player_t(session_id)
    player.nick_name = session_id
    player.password  = session_id
    player.online_time = online_time
    player.ip          = ip
    player.gate_name   = gate_name
    ffext.singleton(player_mgr_t).add(player.id(), player)
    ffext.on_verify_auth_callback(player.id(), "", cb_id)
    ffext.LOGINFO("FFSCENE", "session 认证完成 {0}".format(session_id))

def OnGetUseSessonCb(dictRet, listBindData):
    print("OnGetUseSessonCb ", dictRet, listBindData)
    szAuthKey, online_time, ip, gate_name, cb_id = listBindData
    nFlag = dictRet[dbs_def.FLAG]
    if nFlag is True:
        pass
    else:
        ffext.LOGINFO("FFSCENE", "session not test falg flase.")
        ffext.on_verify_auth_callback(0, "", cb_id)
        return

    listRet = dictRet[dbs_def.RESULT]
    if len(listRet) == 0:
        # no session, craete it
        ffext.LOGINFO("FFSCENE", "session not exist request 2 register session {0}".format(szAuthKey))
        dbs_client.DoAsynCall(rpc_def.DbsCreateUserSession, szAuthKey, funCb=OnCreateUserSessionCb, callbackParams=[online_time, ip, gate_name, cb_id])
        return

    session_id = int(listRet[0][0])
    if ffext.singleton(player_mgr_t).get(session_id) is not None:
        ffext.on_verify_auth_callback(0, "player is on line.", cb_id)
        return

    player = player_t(session_id)
    player.nick_name = session_id
    player.password  = session_id
    player.online_time = online_time
    player.ip          = ip
    player.gate_name   = gate_name
    ffext.singleton(player_mgr_t).add(player.id(), player)
    ffext.on_verify_auth_callback(player.id(), "", cb_id)
    ffext.LOGINFO("FFSCENE", "session 认证完成 {0}".format(session_id))

@ffext.session_verify_callback
def real_session_verify(szAuthKey, online_time, ip, gate_name, cb_id):
    '''
    '''
    print("real_session_verify ", szAuthKey, online_time, ip, gate_name, cb_id)
    req_login = login_pb2.request_login()
    try:
        req_login.ParseFromString(szAuthKey)
    except:
        return []

    szAuthKey = req_login.auth_info
    dbs_client.DoAsynCall(rpc_def.DbsGetUserSession, szAuthKey, funCb=OnGetUseSessonCb, callbackParams=[szAuthKey, online_time, ip, gate_name, cb_id])
    return []

    # print('real_session_verify用户名[%s]对应的id[%s]'%(player.nick_name, player.id()))
    # #异步载入数据库中的数据
    # def callback():
    #     print('real_session_verify载入数据库数据完成%s'%(player.nick_name))

    # dbservice.load_player(player, callback)
    # return [str(player.id())]


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




