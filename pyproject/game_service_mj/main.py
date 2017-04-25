# -*- coding: utf-8 -*-
# @Author  : jh.feng

import ffext, ff
import sys, json
sys.path.append("./pyproject")

from rpc.rpc_property_def import RpcProperty
import rpc.rpc_def as rpc_def
import game_service_mj.logic_mj.mj_mgr as mj_mgr


@ffext.reg_service(rpc_def.Room2MjOnRoomMemberEnter)
def Room2MjOnRoomMemberEnter(dictData):
    ffext.LOGINFO("FFSCENE_PYTHON", "Room2MjOnRoomMemberEnter {0}".format(json.dumps(dictData)))
    mj_mgr._mjMgr.OnPlayerEnterScene(dictData["member"], dictData["room_id"])

@ffext.reg_service(rpc_def.Room2MjOnRoomMemberOffline)
def Room2MjOnRoomMemberOffline(dictData):
    ffext.LOGINFO("FFSCENE_PYTHON", "Room2MjOnRoomMemberOffline {0}".format(json.dumps(dictData)))
    mj_mgr._mjMgr.OnPlayerLeaveScene(dictData["member"])

@ffext.reg_service(rpc_def.Room2MjStartGame)
def RoomCenter2MjStartGame(dictRoomSerial):
    ffext.LOGINFO("FFSCENE_PYTHON", "RoomCenter2MjStartGame {0}".format(json.dumps(dictRoomSerial)))
    mj_mgr.CreateMjRoomService(dictRoomSerial)
    return {RpcProperty.ret: {"id": dictRoomSerial["id"],
                              "scene": ff.service_name}}
