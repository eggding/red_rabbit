# -*- coding: utf-8 -*-
# @Author  : jh.feng

import ffext
import json
import copy
import rpc.rpc_def as rpc_def
import db.dbs_client as dbs_client
import db.dbs_def as dbs_def

g_szCurConfigName = None
g_dictAllGmConfig = {}

def GetCurrentConfig():
    global g_szCurConfigName
    if g_szCurConfigName is None or len(g_szCurConfigName) == 0:
        return {}

    global g_dictAllGmConfig
    return copy.deepcopy(g_dictAllGmConfig[g_szCurConfigName])

def SaveAllConfig():
    global g_dictAllGmConfig, g_szCurConfigName
    dictCopy = copy.deepcopy(g_dictAllGmConfig)

    if g_szCurConfigName is not None:
        dictCopy["g_szCurConfigName"] = g_szCurConfigName
    else:
        dictCopy["g_szCurConfigName"] = ""

    dbs_client.DoAsynCall(rpc_def.DbsSaveAllGmConfig, 0, json.dumps(dictCopy))

def OnLoadAllConfigCb(dictDbRet, nPlayerGID):
    assert dictDbRet[dbs_def.FLAG] is True
    if 0 == len(dictDbRet[dbs_def.RESULT]):
        return
    _, dictData = dictDbRet[dbs_def.RESULT][0]
    print("OnLoadAllConfigCb dictDbRet ", dictData)

    global g_dictAllGmConfig
    global g_szCurConfigName
    g_dictAllGmConfig = json.loads(dictData)
    if "g_szCurConfigName" in g_dictAllGmConfig:
        g_szCurConfigName = g_dictAllGmConfig["g_szCurConfigName"]
        g_dictAllGmConfig.pop("g_szCurConfigName")

def LoadAllConfig():
    dbs_client.DoAsynCall(rpc_def.DbsGetAllGmConfig, 0, None, funCb=OnLoadAllConfigCb, callbackParams=0)

@ffext.reg_service(rpc_def.Gas2GccQueryGmConfig)
def Gas2GccQueryGmConfig(dictData):
    global g_dictAllGmConfig, g_szCurConfigName
    dictCopy = copy.deepcopy(g_dictAllGmConfig)
    dictCopy["g_szCurConfigName"] = g_szCurConfigName
    return dictCopy

@ffext.reg_service(rpc_def.Gas2GccModifyGmConfig)
def Gas2GccModifyGmConfig(dictData):
    global g_szCurConfigName
    import proto.gm_config_pb2 as gm_config_pb2
    nOptType = dictData["opt_type"]
    if nOptType == gm_config_pb2.gm_config_opt.Value("delete"):
        szName = dictData["config_name"]
        del g_dictAllGmConfig[szName]

        if szName == g_szCurConfigName:
            g_szCurConfigName = None

    elif nOptType == gm_config_pb2.gm_config_opt.Value("modify"):
        szName = dictData["config_name"]

        dictRet = {}
        for i in xrange(1, 5):
            szTmp = dictData["pos_{0}_card".format(i)]
            nLen = len(map(int, szTmp.split(",")))
            dictRet[nLen] = dictRet.get(nLen, 0) + 1

        assert len(dictRet) == 2
        assert sum(dictRet.keys()) == (13 + 14)

        g_dictAllGmConfig[szName] = dictData

    elif nOptType == gm_config_pb2.gm_config_opt.Value("apply"):
        szName = dictData["config_name"]
        if szName not in g_dictAllGmConfig:
            return
        g_szCurConfigName = szName

    SaveAllConfig()

    return {"opt_type": nOptType,
            "conf_name": g_szCurConfigName,
            "dict_data": dictData}