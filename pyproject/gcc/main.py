# -*- coding: utf-8 -*-
# @Author  : jh.feng

import sys
import ffext, ff

sys.path.append("./pyproject")
import rpc.rpc_def as rpc_def
import rpc.scene_def as scene_def
import gcc.gcc_scene.gcc_scene_mgr as gcc_scene_mgr
import gcc.gcc_room_mgr.gcc_room_mgr as gcc_room_mgr

# def Tick2SendHttpReq():
#     tick_mgr.RegisterOnceTick(1000, Tick2SendHttpReq)
#     print("Tick2SendHttpReq ")
#     ffext.call_service("http_service", 10001, "say hi")
#
# def Tick2ConnectHttpService():
#     print("Tick2ConnectHttpService")
#     ffext.connect_to_outer_service("http_service", "tcp://127.0.0.1:10500")
#     Tick2SendHttpReq()
#
@ffext.reg_service(rpc_def.OnAllServiceStartUp)
def OnAllServiceStartUp(dictSerial):
    import id_manager.room_id_mgr as room_id_mgr
    room_id_mgr.init()

    import robot.gm_opt_config as gm_opt_config
    gm_opt_config.LoadAllConfig()

@ffext.reg_service(rpc_def.TestService)
def TestService(dictSerial):
    print("test service on ", ff.service_name)
    print(dictSerial)

@ffext.reg_service(rpc_def.Peer)
def Peer(dictSerial):
    ffext.call_service(scene_def.GATE_MASTER, rpc_def.RspPeer, {"service": ff.service_name})

def A():
    ffext.call_service(scene_def.GATE_MASTER, rpc_def.OnServiceConn, {"service": ff.service_name})


import util.tick_mgr as tick_mgr
tick_mgr.RegisterOnceTick(100, A)
