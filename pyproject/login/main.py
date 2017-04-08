# coding=UTF-8
import os
import time
import ffext
import event_bus

import sys
sys.path.append("./pyproject")

import proto.recv_msg_pb2 as recv_msg_pb2
import player_mgr.player_mgr_handler as player_mgr_handler
import rpc.scene_def as scene_def

scene_def.CUR_SCENE_NAME = scene_def.LOGIN_SCENE

class player_mgr_t(object):
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


class player_t(object):
    def __init__(self, session_id_):
        self.session_id = session_id_;
        self.chat_times = 0

    def id():
        return self.session_id

    def inc_chat_times(self):
        self.chat_times += 1

    def get_chat_times(self):
        return self.chat_times


def OnEnterLoginScene(session, src, data):
    print("Onenter login scene ", session, src, data)
    ffext.change_session_scene(session, "scene@1", "oops")

ffext.g_session_enter_callback = OnEnterLoginScene

# 这个修饰器的意思是注册process_chat函数接收cmd=1的消息
@ffext.session_call(1354, recv_msg_pb2.recv_info)
def process_chat(session_id, msg):
    print("session_id, msg ", session_id, msg)
    ffext.send_msg_session(session_id, 2, "xxx 33484gf hello rsp.")
