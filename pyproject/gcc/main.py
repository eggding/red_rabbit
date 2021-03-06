# -*- coding: utf-8 -*-
# @Author  : jh.feng

import sys
import ffext, ff

sys.path.append("./pyproject")
import rpc.rpc_def as rpc_def
import rpc.scene_def as scene_def
import gcc.gcc_scene.gcc_scene_mgr as gcc_scene_mgr
import gcc.gcc_room_mgr.gcc_room_mgr as gcc_room_mgr
import service_ex.service_base as service_base
#
@ffext.reg_service(rpc_def.OnAllServiceStartUp)
def OnAllServiceStartUp(dictSerial):
    import id_manager.room_id_mgr as room_id_mgr
    room_id_mgr.init()

    import robot.gm_opt_config as gm_opt_config
    gm_opt_config.LoadAllConfig()

@ffext.reg_service(rpc_def.Peer)
def Peer(dictSerial):
    ffext.call_service(scene_def.GATE_MASTER, rpc_def.RspPeer, {"service": ff.service_name})

def A():
    ffext.call_service(scene_def.GATE_MASTER, rpc_def.OnServiceConn, {"service": ff.service_name})


import util.tick_mgr as tick_mgr
tick_mgr.RegisterOnceTick(100, A)
