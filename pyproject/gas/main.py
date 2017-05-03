# -*- coding: utf-8 -*-
# @Author  : jh.feng

import ffext
import sys
sys.path.append("./pyproject")

import conf as conf
import rpc.rpc_def as rpc_def
import entity.entity_mgr as entity_mgr
import gas.gas_scene.gas_scene_mgr as gas_scene_mgr
import excel2json as excel2json

excel2json.LoadAllCfg()

@ffext.session_call(rpc_def.Gac2GasExeCode)
def Gac2GasExeCode(nPlayerGID, szCode):
    if conf.dict_cfg["debug_env"] is False:
        return

    szCode = szCode["0"]

    Player = entity_mgr.GetEntity(nPlayerGID)
    assert Player is not None

    print(szCode)
    exec(szCode)

