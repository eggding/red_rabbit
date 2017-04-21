# -*- coding: utf-8 -*-
# @Author  : jh.feng

import ffext
import sys, json
sys.path.append("./pyproject")

import rpc.rpc_def as rpc_def
import game_service_mj.logic_mj.mj_mgr as mj_mgr

@ffext.reg_service(rpc_def.Room2MjStartGame)
def RoomCenter2MjStartGame(szScene, dictRoomSerial):
    ffext.LOGINFO("FFSCENE_PYTHON", "RoomCenter2MjStartGame {0}".format(szScene))
    pass
