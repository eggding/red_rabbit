# coding=UTF-8
import ffext, ff
import sys
sys.path.append("./pyproject")

import rpc.rpc_def as rpc_def
import rpc.scene_def as scene_def
import login.login_mgr as login_mgr
import service_ex.service_base as service_base

@ffext.reg_service(rpc_def.OnAllServiceStartUp)
def OnAllServiceStartUp(dictSerial):
    pass

@ffext.reg_service(rpc_def.Peer)
def Peer(dictSerial):
    ffext.call_service(scene_def.GATE_MASTER, rpc_def.RspPeer, {"service": ff.service_name})


def A():
    ffext.call_service(scene_def.GATE_MASTER, rpc_def.OnServiceConn, {"service": ff.service_name})

import util.tick_mgr as tick_mgr
tick_mgr.RegisterOnceTick(100, A)
