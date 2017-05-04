# -*- coding: utf-8 -*-
# @Author  : jh.feng

import ffext as framework
import white_list as white_list
import rpc.rpc_def as rpc_def

g_dictToken = {
    "585231e1353e9d56e284b8a9": True,
}

def IsTokenValid(szToken, ip):
    print("test token ", szToken, ip)

    if ip not in white_list.dict_white_list:
        return False

    global g_dictToken
    bValid = g_dictToken.get(szToken, False)
    return bValid

def SendCode(szScene, szCode):
    if "all_gas" == szScene:
        import conf as conf
        nGasNum = conf.dict_cfg["gas"]["num"]
        for i in xrange(0, nGasNum):
            szScene = "gas@{0}".format(i)
            framework.call_service(szScene, rpc_def.All2ExeCode, {"code": szCode})
    else:
        framework.call_service(szScene, rpc_def.All2ExeCode, {"code": szCode})

def ExeCode(szCode, nPlayerGID=None):
    Player = None
    if nPlayerGID is not None:
        import entity.entity_mgr as entity_mgr
        Player = entity_mgr.GetEntity(nPlayerGID)
    exec(szCode)
    framework.LOGINFO("FFSCENE_PYTHON", "GmTool.ExeCode {0}".format(szCode))
