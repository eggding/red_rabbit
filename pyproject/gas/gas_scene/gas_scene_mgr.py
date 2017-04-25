# -*- coding: utf-8 -*-
# @Author  : jh.feng

import json
import ffext, ff
import util.util as util
import conf as conf
import entity.entity_mgr as entity_mgr
import db.dbs_client as dbs_client
import db.dbs_def as dbs_def
import rpc.rpc_def as rpc_def
import rpc.scene_def as scene_def
import entity.gas_player_entity as gas_player_entity
import residual.residual_mgr as residual_mgr

class GasSceneMgr(object):
    def __init__(self):
        self.m_residualMgr = residual_mgr.ResidualMgr(self)

    def OnLoadPlayerDataDone(self, dictSerialData, szSerial):
        assert dictSerialData[dbs_def.FLAG] is True

        dictExtra = json.loads(szSerial)
        util.dict_merge(json.loads(dictExtra), dictSerialData)

        ffext.LOGINFO("FFSCENE_PYTHON", "OnLoadPlayerDataDone {0}".format(json.dumps(dictSerialData)))
        gasPlayer = gas_player_entity.GasPlayerEntity()
        gasPlayer.InitFromDict(dictSerialData)
        entity_mgr.AddEntity(gasPlayer.GetGlobalID(), gasPlayer)
        ffext.call_service(scene_def.GCC_SCENE, rpc_def.Gas2GccSynPlayerGasID, {"id": gasPlayer.GetGlobalID(),
                                                                                "scene": ff.service_name})

    def Gcc2GasSessionConn(self, nPlayerGID, szSerial):
        ffext.LOGINFO("FFSCENE_PYTHON", "GasSceneMgr.Login2GccSessionConn {0}, {1}".format(nPlayerGID, szSerial))
        gasPlayer = entity_mgr.GetEntity(nPlayerGID)
        if gasPlayer is not None:
            if self.m_residualMgr.IsPlayerInResidual(nPlayerGID) is True:
                self.m_residualMgr.RemoveResidualPlayer(nPlayerGID)
        else:
            dbs_client.DoAsynCall(rpc_def.DbsLoadPlayerData, nPlayerGID, 0, nChannel=nPlayerGID, funCb=self.OnLoadPlayerDataDone, callbackParams=szSerial)

    def OnPlayerOffline(self, nPlayerGID):
        ffext.LOGINFO("FFSCENE_PYTHON", "GasSceneMgr.OnPlayerOffline {0}".format(nPlayerGID, nPlayerGID))
        self.m_residualMgr.AddResidualPlayer(nPlayerGID)

    def PlayerTrueOffline(self, nPlayerGID):
        ffext.LOGINFO("FFSCENE_PYTHON", "player true offline {0}".format(nPlayerGID))
        Player = entity_mgr.GetEntity(nPlayerGID)
        if Player is not None:
            Player.Destroy()
        entity_mgr.DelEntity(nPlayerGID)

        # self.ExitRoom(nPlayerGID)

_gasSceneMgr = GasSceneMgr()

@ffext.reg_service(rpc_def.Gcc2GasPlayerOffline)
def Gcc2GasPlayerOffline(dictData):
    nPlayerGID = dictData["id"]
    _gasSceneMgr.OnPlayerOffline(nPlayerGID)

@ffext.session_enter_callback
def Gcc2GasSessionConn(nPlayerGID, szSrcScene, szSerial):
    _gasSceneMgr.Gcc2GasSessionConn(nPlayerGID, szSerial)


