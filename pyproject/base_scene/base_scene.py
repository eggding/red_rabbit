# -*- coding: utf-8 -*-
# @Author  : jh.feng

import ffext
import util.util as util
import rpc.rpc_def as rpc_def
import entity.entity_mgr as entity_mgr

class BaseScene(object):
    def __init__(self):
        pass

import proto.change_scene_pb2 as change_scene_pb2
@ffext.session_call(rpc_def.Gac2GasChangeScene, change_scene_pb2.change_scene_req)
def Gac2GasRequestChangeScene(nPlayerGID, reqObj):
    szDstScene = reqObj.scene_name
    if util.IsGasScene(szDstScene) is False:
        return

    Player = entity_mgr.GetEntity(nPlayerGID)
    if Player is None:
        return

    bRet = Player.RequestChangeScene(szDstScene)
    if bRet is False:
        ffext.


