# -*- coding: utf-8 -*-
# @Author  : jh.feng

import ffext
import json
import rpc.rpc_def as rpc_def
import db.dbs_client as dbs_client
import db.dbs_def as dbs_def
import proto.gm_config_pb2 as gm_config_pb2

def OnLoadAllConfigCb(dictDbRet, nPlayerGID):
    print("OnLoadAllConfigCb dictDbRet ", dictDbRet)
    assert dictDbRet[dbs_def.FLAG] is True
    listRet = dictDbRet[dbs_def.RESULT]
    rsp = gm_config_pb2.load_config_rsp()
    rsp.ret = 0
    for tupleOneRet in listRet:
        nID, dictConf = tupleOneRet
        rsp.conf_arr.append(json.dumps(dictConf))
    ffext.send_msg_session(nPlayerGID, rpc_def.Gas2GacRetLoadAllConfig, rsp.SerializeToString())

def Test():
    dbs_client.DoAsynCall(rpc_def.DbsGetAllGmConfig, 0, None, funCb=OnLoadAllConfigCb, callbackParams=0)

@ffext.session_call(rpc_def.Gac2GasLoadAllConfig, gm_config_pb2.load_config_req)
def Gac2GasLoadAllConfig(nPlayerGID, reqObj):
    dbs_client.DoAsynCall(rpc_def.DbsGetAllGmConfig, 0, None, funCb=OnLoadAllConfigCb, callbackParams=nPlayerGID)