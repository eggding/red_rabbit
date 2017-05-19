# -*- coding: utf-8 -*-
# @Author  : jh.feng

import ffext
import json
import copy
import rpc.rpc_def as rpc_def
import db.dbs_client as dbs_client
import db.dbs_def as dbs_def
import proto.gm_config_pb2 as gm_config_pb2

g_szCurConfigName = None
g_dictAllGmConfig = {}

def SaveAllConfig():
    global g_dictAllGmConfig, g_szCurConfigName
    dictCopy = copy.deepcopy(g_dictAllGmConfig)

    if g_szCurConfigName is not None:
        dictCopy["g_szCurConfigName"] = g_szCurConfigName
    else:
        dictCopy["g_szCurConfigName"] = ""

    dbs_client.DoAsynCall(rpc_def.DbsSaveAllGmConfig, 0, json.dumps(dictCopy))

    # import conf as conf
    # nGasNum = conf.dict_cfg["gas"]["num"]
    # for i in xrange(0, nGasNum):
    #     ffext.call_service("gas@{0}".format(i), rpc_def.AllGasUpdateGmConfig, dictCopy)

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
    reqObj = gm_config_pb2.opt_config_req()
    reqObj.ParseFromString(dictData["data"])
    nOptType = reqObj.opt_type
    dictTmp = {}
    if nOptType == gm_config_pb2.gm_config_opt.Value("delete"):
        szName = reqObj.conf_data.config_name
        del g_dictAllGmConfig[szName]

    elif nOptType == gm_config_pb2.gm_config_opt.Value("modify"):
        szName = reqObj.conf_data.config_name
        dictTmp = {
            "config_name": reqObj.conf_data.config_name,
            "pos_1_card": reqObj.conf_data.pos_1_card,
            "pos_2_card": reqObj.conf_data.pos_2_card,
            "pos_3_card": reqObj.conf_data.pos_3_card,
            "pos_4_card": reqObj.conf_data.pos_4_card,
            "card_order": reqObj.conf_data.card_order,
        }
        g_dictAllGmConfig[szName] = dictTmp

    elif nOptType == gm_config_pb2.gm_config_opt.Value("apply"):
        szName = reqObj.conf_data.config_name
        if szName not in g_dictAllGmConfig:
            return
        g_szCurConfigName = szName

    SaveAllConfig()

    return {"opt_type": nOptType,
            "conf_name": g_szCurConfigName,
            "dict_data": dictTmp}