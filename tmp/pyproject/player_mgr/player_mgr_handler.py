# -*- coding: utf-8 -*-
from player_mgr_model import *
import ffext
import msg_def.ttypes as msg_def
from db import dbservice


import thrift.Thrift as Thrift
import thrift.protocol.TBinaryProtocol as TBinaryProtocol
import thrift.protocol.TCompactProtocol as TCompactProtocol
import thrift.transport.TTransport as TTransport

@ffext.session_verify_callback
def real_session_verify(session_key, online_time, ip, gate_name):
    '''
    '''
    account = msg_def.account_t()
    # ffext.decode_buff(account, session_key)

    player = player_t(session_key)
    player.nick_name = session_key
    player.password  = session_key
    #注册账号请求
    # if account.register_flag == True:
    #     if False == dbservice.register_player(player):
    #         return []
    # elif False == dbservice.verify_password(player):
    #     return []
    player.online_time = online_time
    player.ip          = ip
    player.gate_name   = gate_name
    ffext.singleton(player_mgr_t).add(player.id(), player)

    print('real_session_verify用户名[%s]对应的id[%s]'%(player.nick_name, player.id()))
    #异步载入数据库中的数据
    def callback():
        print('real_session_verify载入数据库数据完成%s'%(player.nick_name))

    dbservice.load_player(player, callback)
    return [str(player.id())]


@ffext.session_enter_callback
def real_session_enter(session_id, from_scene, extra_data):
    print("real_session_enter ", session_id)


@ffext.session_offline_callback
def real_session_offline(session_id, online_time):
    print("real_session_offline ", session_id)
    ffext.singleton(player_mgr_t).remove(session_id)

						



