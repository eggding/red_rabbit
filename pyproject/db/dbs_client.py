# -*- coding:utf-8 -*-

import json
import ffext
import rpc.rpc_def as rpc_def
import rpc.scene_def as scene_def
import dbs_def as dbs_def
import ff

g_nCbSerial = 0
g_dictSerial2CbInfo = {}

def GenCbSerial():
    global g_nCbSerial
    g_nCbSerial += 1
    return g_nCbSerial

def DoAsynCall(cmd, session, sendParams, funCb=None, callbackParams=None, nChannel=None):
    nCbID = GenCbSerial()
    global g_dictSerial2CbInfo
    g_dictSerial2CbInfo[nCbID] = [funCb, callbackParams]

    dictPacket = {
        dbs_def.PARAMS: sendParams,
        dbs_def.SRC_SCENE: ff.service_name,
        dbs_def.CB_ID: nCbID,
        dbs_def.SESSION: session
    }
    if nChannel is None:
        dictPacket[dbs_def.USE_CHANNEL] = 0
        ffext.call_service(scene_def.DB_SERVICE_DEFAULT, cmd, json.dumps(dictPacket))
    else:
        nChannel = int(nChannel)
        nDbQueueID = nChannel % 1
        dictPacket[dbs_def.USE_CHANNEL] = nChannel
        ffext.call_service(scene_def.DB_SERVICE_DEFAULT + str(nDbQueueID), cmd, json.dumps(dictPacket))

@ffext.reg_service(rpc_def.OnDbAsynCallReturn)
def OnDbAsynCallReturn(dictRet):

    nCbId = dictRet[dbs_def.CB_ID]
    global g_dictSerial2CbInfo
    listData = g_dictSerial2CbInfo.get(nCbId)
    g_dictSerial2CbInfo.pop(nCbId)
    if listData is None:
        return

    funCb, params = listData
    if funCb is None:
        return

    if params is not None:
        funCb(dictRet, params)
    else:
        funCb(dictRet)
