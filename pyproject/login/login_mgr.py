# -*- coding:utf-8 -*-
import ff
import ffext
import proto.login_pb2 as login_pb2
import db.dbs_client as dbs_client
import rpc.rpc_def as rpc_def
import db.dbs_def as dbs_def
import entity.player_in_login as player_in_login
import json
import rpc.scene_def as scene_def
import util.gm_tool as gm_tool

class LoginMgr(object):
    def __init__(self):
        self.all_players = {}

    def get(self, session_id_):
        return self.all_players.get(session_id_)

    def remove(self, session_id_):
        del self.all_players[session_id_]

    def add(self, session_id_, player):
        self.all_players[session_id_] = player

    def size(self):
        return len(self.all_players)

    def idlist(self):
        return self.all_players.keys()

_loginMgr = LoginMgr()


def OnCreateUserSessionCb(dictRet, listBindData):
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
    player = player_in_login.PlayerInLogin(session_id, online_time, ip, gate_name)
    _loginMgr.add(session_id, player)
    ffext.on_verify_auth_callback(player.GetGlobalID(), "", cb_id)
    ffext.LOGINFO("FFSCENE", "session auth ok {0}".format(session_id))

def OnGetUseSessonCb(dictRet, listBindData):
    # print("OnGetUseSessonCb ", dictRet, listBindData)
    szAuthKey, online_time, ip, gate_name, cb_id = listBindData
    nFlag = dictRet[dbs_def.FLAG]
    if nFlag is True:
        pass
    else:
        ffext.LOGINFO("FFSCENE", "session not test falg flase.")
        ffext.on_verify_auth_callback(0, "", cb_id)
        return

    session_id = dictRet[dbs_def.RESULT]
    if session_id == 0:
        # no session, craete it
        # ffext.LOGINFO("FFSCENE", "session not exist request 2 register session {0}".format(szAuthKey))
        # dbs_client.DoAsynCall(rpc_def.DbsCreateUserSession, 0, szAuthKey, funCb=OnCreateUserSessionCb, callbackParams=[online_time, ip, gate_name, cb_id])
        ffext.on_verify_auth_callback(0, "err.", cb_id)
        return

    if _loginMgr.get(session_id) is not None:
        ffext.on_verify_auth_callback(0, "player is online.", cb_id)
        print("player online ...")
        return

    player = player_in_login.PlayerInLogin(session_id, online_time, ip, gate_name)
    _loginMgr.add(session_id, player)
    ffext.on_verify_auth_callback(player.GetGlobalID(), "", cb_id)
    ffext.LOGINFO("FFSCENE", "session auth ok {0}".format(session_id))

@ffext.session_verify_callback
def real_session_verify(szAuthKey, online_time, ip, gate_name, cb_id):
    """
    Auth.
    :param szAuthKey:
    :param online_time:
    :param ip:
    :param gate_name:
    :param cb_id:
    :return:
    """

    if _loginMgr.size() > 2000:
        ffext.on_verify_auth_callback(0, "", cb_id)
        return []

    print("real_session_verify ", szAuthKey, online_time, ip, gate_name, cb_id)
    req_login = login_pb2.login_req()
    try:
        req_login.ParseFromString(szAuthKey)
    except:
        print("req_login.ParseFromString error! ")
        return []

    print("req_login.type ", req_login.type)

    nType = req_login.type
    if nType == login_pb2.login_type.Value("get_gate_info"):
        def _retGetGateAddr(err, msg):
            szGateAddr = msg["gate_info"]
            rsp = login_pb2.login_rsp()
            rsp.ret = 0
            rsp.gate_info = szGateAddr.encode("utf-8")
            ffext.on_verify_auth_callback(0, rsp.SerializeToString(), cb_id)
        ffext.call_service(scene_def.GATE_MASTER, rpc_def.GetGateIp, {"0": 0}, _retGetGateAddr)
        return []

    elif nType == login_pb2.login_type.Value("login"):
        szAuthKey = req_login.auth_info
        dbs_client.DoAsynCall(rpc_def.DbsGetUserSession, 0, szAuthKey, funCb=OnGetUseSessonCb, callbackParams=[szAuthKey, online_time, ip, gate_name, cb_id])
        return []

    elif nType == login_pb2.login_type.Value("gm_code"):
        # gm
        szToken, szScene, szCode = req_login.auth_info.split("#")
        if gm_tool.IsTokenValid(szToken, ip) is False:
            ffext.on_verify_auth_callback(0, "", cb_id)
        else:
            gm_tool.SendCode(szScene, szCode)
        return []

    else:
        ffext.on_verify_auth_callback(0, "", cb_id)
        return []

@ffext.session_offline_callback
def real_session_offline(session_id, online_time):
    import rpc.scene_def as scene_def
    import rpc.rpc_def as rpc_def
    ffext.LOGINFO("FFSCENE_PYTHON", "real_session_offline {0}, last scene {1}".format(session_id, ff.service_name))

    loginPlayer = GetPlayer(session_id)
    assert loginPlayer is not None
    _loginMgr.remove(session_id)

    ffext.call_service(scene_def.GCC_SCENE, rpc_def.Login2GccPlayerOffline, {"id": session_id})

    # gate master
    ffext.call_service(scene_def.GATE_MASTER, rpc_def.OnSessionDisConnGate, {"player_id": loginPlayer.GetGlobalID(),
                                                                             "gate_id": loginPlayer.GetGateName()})

def GetPlayer(nPlayerGID):
    return _loginMgr.get(nPlayerGID)

@ffext.session_enter_callback
def OnEnterLoginScene(session, src, data):
    loginPlayer = GetPlayer(session)
    assert loginPlayer is not None

    rsp = login_pb2.login_rsp()
    rsp.ret = 0
    rsp.player_id = session
    ffext.send_msg_session(session, rpc_def.ResponseLogin, rsp.SerializeToString())

    # gate master
    ffext.call_service(scene_def.GATE_MASTER, rpc_def.OnSessionConnectGate, {"player_id": loginPlayer.GetGlobalID(),
                                                                             "gate_id": loginPlayer.GetGateName()})

    ffext.change_session_scene(session, scene_def.GCC_SCENE, json.dumps(loginPlayer.Serial2Dict()))
    ffext.LOGINFO("FFSCENE_PYTHON", "Auth done, request change scene 2 gcc {0}, {1}".format(session, json.dumps(loginPlayer.Serial2Dict())))
