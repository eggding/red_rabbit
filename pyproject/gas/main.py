# -*- coding: utf-8 -*-
# @Author  : jh.feng

import ffext, ff
import sys
sys.path.append("./pyproject")

import cProfile
import StringIO, pstats
import service_ex.service_base as service_base

pr = cProfile.Profile()
pr.enable()

g_nProfileSeconds = 60

import util.tick_mgr as tick_mgr
def Tick2DumpProfile():
    pass
    # tick_mgr.RegisterOnceTick(g_nProfileSeconds * 1000, Tick2DumpProfile)
    # s = StringIO.StringIO()
    # # sortby = 'cumulative'
    # ps = pstats.Stats(pr, stream=s)# .sort_stats(sortby)
    # ps.print_stats()
    # aa = s.getvalue()
    # with open('./profile_{0}.out'.format(ff.service_name),'w') as f:
    #     f.write(aa)


import excel2json as excel2json
excel2json.LoadAllCfg()


import conf as conf
import rpc.rpc_def as rpc_def
import rpc.scene_def as scene_def
import entity.entity_mgr as entity_mgr
import gas.gas_scene.gas_scene_mgr as gas_scene_mgr

@ffext.reg_service(rpc_def.OnAllServiceStartUp)
def OnAllServiceStartUp(dictSerial):
    import robot.robot_mgr as robot_mgr
    import robot.gas_gm_config_opt as gas_gm_config_opt

@ffext.reg_service(rpc_def.Peer)
def Peer(dictSerial):
    ffext.call_service(scene_def.GATE_MASTER, rpc_def.RspPeer, {"service": ff.service_name})

@ffext.session_call(rpc_def.Gac2GasExeCode)
def Gac2GasExeCode(nPlayerGID, szCode):
    if conf.dict_cfg["debug_env"] is False:
        return

    szCode = szCode["0"]
    import util.gm_tool as gm_tool
    gm_tool.ExeCode(szCode, nPlayerGID)

def A():
    ffext.call_service(scene_def.GATE_MASTER, rpc_def.OnServiceConn, {"service": ff.service_name})

tick_mgr.RegisterOnceTick(100, A)
