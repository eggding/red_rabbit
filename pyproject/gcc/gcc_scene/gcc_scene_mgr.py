# -*- coding: utf-8 -*-
# @Author  : jh.feng

import json
import ffext
import random
import conf as conf
import rpc.rpc_def as rpc_def
import util.enum_def as enum_def
import entity.entity_mgr as entity_mgr
import entity.gcc_player_entity as gcc_player_entity

from db.table.table_property_def import Player as PlayerPro

class GccSceneMgr(object):
    def __init__(self):
        self.m_nGasNum = conf.dict_cfg["gas"]["num"]

    def ChooseOneGas(self):
        ret = random.randint(0, 10000)
        return "gas@{0}".format(ret % self.m_nGasNum)

    def Login2GccSessionConn(self, nPlayerGID, szSerial):
        ffext.LOGINFO("FFSCENE_PYTHON", "GccSceneMgr.Login2GccSessionConn {0}, {1}".format(nPlayerGID, szSerial))
        gccPlayer = entity_mgr.GetEntity(nPlayerGID)
        if gccPlayer is not None:
            gccPlayer.SetState(enum_def.EPlayerState.eOnline)
            ffext.change_session_scene(nPlayerGID, gccPlayer.GetGasID(), "")
        else:
            dictSerial = json.loads(szSerial)
            gccPlayer = gcc_player_entity.GccPlayerEntity()
            gccPlayer.SetIp(dictSerial[PlayerPro.IP])
            gccPlayer.SetGateName(dictSerial[PlayerPro.GATE_NAME])
            gccPlayer.SetState(enum_def.EPlayerState.eOnline)
            entity_mgr.AddEntity(nPlayerGID, gccPlayer)
            ffext.change_session_scene(nPlayerGID, self.ChooseOneGas(), szSerial)

    def Gas2GccSynPlayerGasID(self, nPlayerGID, szGasID):
        ffext.LOGINFO("FFSCENE_PYTHON", "GccSceneMgr.Gas2GccSynPlayerGasID {0}, {1}".format(nPlayerGID, szGasID))
        gccPlayer = entity_mgr.GetEntity(nPlayerGID)
        assert gccPlayer is not None
        gccPlayer.SetGasID(szGasID)

        # check state
        if gccPlayer.GetState() == enum_def.EPlayerState.eDisConnect:
            ffext.call_service(szGasID, rpc_def.Gcc2GasRetSynPlayerState, {"state": gccPlayer.GetState(),
                                                                           "player_id": nPlayerGID})

    def OnPlayerOffline(self, nPlayerGID):
        ffext.LOGINFO("FFSCENE_PYTHON", "GccSceneMgr.OnPlayerOffline {0}".format(nPlayerGID))
        gccPlayer = entity_mgr.GetEntity(nPlayerGID)
        assert gccPlayer is not None
        gccPlayer.SetState(enum_def.EPlayerState.eDisConnect)
        ffext.call_service(gccPlayer.GetGasID(), rpc_def.Gcc2GasPlayerOffline, {"id": nPlayerGID})

    def OnPlayerTrueOffline(self, nPlayerGID):
        ffext.LOGINFO("FFSCENE_PYTHON", "GccSceneMgr.OnPlayerTrueOffline {0}".format(nPlayerGID))
        gccPlayer = entity_mgr.GetEntity(nPlayerGID)
        assert gccPlayer is not None
        gccPlayer.Destroy()
        entity_mgr.DelEntity(nPlayerGID)


_gccSceneMgr = GccSceneMgr()

@ffext.reg_service(rpc_def.All2ExeCode)
def All2ExeCode(dictData):
    szCode = dictData["code"]
    import util.gm_tool as gm_tool
    gm_tool.ExeCode(szCode)

@ffext.reg_service(rpc_def.Gas2GccPlayerTrueOffline)
def Gas2GccPlayerTrueOffline(dictData):
    nPlayerGID = dictData["id"]
    _gccSceneMgr.OnPlayerTrueOffline(nPlayerGID)

@ffext.reg_service(rpc_def.Login2GccPlayerOffline)
def Login2GccPlayerOffline(dictData):
    nPlayerGID = dictData["id"]
    _gccSceneMgr.OnPlayerOffline(nPlayerGID)

@ffext.reg_service(rpc_def.Gas2GccSynPlayerGasID)
def Gas2GccSynPlayerGasID(dictData):
    nPlayerGID, szGasID = dictData["id"], dictData['scene']
    _gccSceneMgr.Gas2GccSynPlayerGasID(nPlayerGID, szGasID)

@ffext.session_enter_callback
def Login2GccSessionConn(nPlayerGID, szSrcScene, szSerial):
    _gccSceneMgr.Login2GccSessionConn(nPlayerGID, szSerial)

