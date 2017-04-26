# -*- coding: utf-8 -*-
# @Author  : jh.feng

import json
import ffext, ff
import util.util as util
import entity.entity_mgr as entity_mgr
import db.dbs_client as dbs_client
import db.dbs_def as dbs_def
import rpc.rpc_def as rpc_def
import rpc.scene_def as scene_def
import entity.gas_player_entity as gas_player_entity
import residual.residual_mgr as residual_mgr
import gas.gas_room_mgr.gas_room_mgr as gas_room_mgr

class GasSceneMgr(object):
    def __init__(self):
        self.m_residualMgr = residual_mgr.ResidualMgr(self)

    def OnLoadPlayerDataDone(self, dictSerialData, szSerial):
        assert dictSerialData[dbs_def.FLAG] is True
        util.dict_merge(json.loads(szSerial), dictSerialData)

        ffext.LOGINFO("FFSCENE_PYTHON", "OnLoadPlayerDataDone {0}".format(json.dumps(dictSerialData)))
        gasPlayer = gas_player_entity.GasPlayerEntity()
        gasPlayer.InitFromDict(dictSerialData)
        gasPlayer.SetScene(self)
        entity_mgr.AddEntity(gasPlayer.GetGlobalID(), gasPlayer)
        ffext.call_service(scene_def.GCC_SCENE, rpc_def.Gas2GccSynPlayerGasID, {"id": gasPlayer.GetGlobalID(),
                                                                                "scene": ff.service_name})

    def Gcc2GasSessionConn(self, nPlayerGID, szSerial):
        ffext.LOGINFO("FFSCENE_PYTHON", "GasSceneMgr.Login2GccSessionConn {0}, {1}".format(nPlayerGID, szSerial))
        gasPlayer = entity_mgr.GetEntity(nPlayerGID)
        if gasPlayer is not None:
            if self.m_residualMgr.IsPlayerInResidual(nPlayerGID) is True:
                self.m_residualMgr.RemoveResidualPlayer(nPlayerGID)
            gas_room_mgr.OnMemberEnter(nPlayerGID)
        else:
            dbs_client.DoAsynCall(rpc_def.DbsLoadPlayerData, nPlayerGID, 0, nChannel=nPlayerGID, funCb=self.OnLoadPlayerDataDone, callbackParams=szSerial)

    def OnPlayerOffline(self, nPlayerGID):
        ffext.LOGINFO("FFSCENE_PYTHON", "GasSceneMgr.OnPlayerOffline {0}".format(nPlayerGID))
        gasPlayer = entity_mgr.GetEntity(nPlayerGID)
        assert gasPlayer is not None

        gas_room_mgr.OnMemberExit(nPlayerGID)
        if gasPlayer.GetRoomID() is not None:
            self.m_residualMgr.AddResidualPlayer(nPlayerGID)
        else:
            self.PlayerTrueOffline(nPlayerGID)

    def PlayerTrueOffline(self, nPlayerGID):
        ffext.LOGINFO("FFSCENE_PYTHON", "GasSceneMgr.PlayerTrueOffline {0}".format(nPlayerGID))
        Player = entity_mgr.GetEntity(nPlayerGID)
        if Player is not None:
            Player.Destroy()
        entity_mgr.DelEntity(nPlayerGID)

        ffext.call_service(scene_def.GCC_SCENE, rpc_def.Gas2GccPlayerTrueOffline, {"id": nPlayerGID})

    def OnPlayerGameEnd(self, nPlayerGID):
        if self.m_residualMgr.IsPlayerInResidual(nPlayerGID) is True:
            self.m_residualMgr.RemoveResidualPlayer(nPlayerGID)
            self.PlayerTrueOffline(nPlayerGID)

    def OnPlayerChangeScene(self, nPlayerGID, szSerial):
        ffext.LOGINFO("FFSCENE_PYTHON", "OnPlayerChangeScene {0}".format(szSerial))
        Player = entity_mgr.GetEntity(nPlayerGID)
        assert Player is None
        Player = gas_player_entity.GasPlayerEntity()
        dictSerial = json.loads(szSerial)
        Player.DeSerial(dictSerial)
        Player.SetScene(self)
        entity_mgr.AddEntity(nPlayerGID, Player)
        ffext.call_service(scene_def.GCC_SCENE, rpc_def.Gas2GccSynPlayerGasID, {"id": Player.GetGlobalID(),
                                                                                "scene": ff.service_name})
        if "room_id" in dictSerial:
            nRoomID = dictSerial["room_id"]
            gas_room_mgr.EnterRoom(nPlayerGID, nRoomID)

_gasSceneMgr = GasSceneMgr()

@ffext.reg_service(rpc_def.Gcc2GasPlayerOffline)
def Gcc2GasPlayerOffline(dictData):
    nPlayerGID = dictData["id"]
    _gasSceneMgr.OnPlayerOffline(nPlayerGID)

@ffext.reg_service(rpc_def.Gcc2GasRetSynPlayerState)
def Gcc2GasRetSynPlayerState(dictData):
    nPlayerGID = dictData["player_id"]
    nState = dictData["state"]
    from util.enum_def import EPlayerState
    if nState == EPlayerState.eDisConnect:
        if _gasSceneMgr.m_residualMgr.IsPlayerInResidual(nPlayerGID) is False:
            _gasSceneMgr.m_residualMgr.AddResidualPlayer(nPlayerGID)

@ffext.session_enter_callback
def OnEnteredGasScene(nPlayerGID, szSrcScene, szSerial):
    if szSrcScene == scene_def.GCC_SCENE:
        _gasSceneMgr.Gcc2GasSessionConn(nPlayerGID, szSerial)
    elif util.IsGasScene(szSrcScene) is True:
        _gasSceneMgr.OnPlayerChangeScene(nPlayerGID, szSerial)
    else:
        assert False


