# -*- coding: utf-8 -*-
# @Author  : jh.feng

import ff, ffext
import rpc.rpc_def as rpc_def
import db.dbs_client as dbs_client
import db.dbs_def as dbs_def
import gcc_room_obj as gcc_room_obj

class GccRoomMgr(object):
    def __init__(self):
        self.m_nRoomIDBegin = 0
        self.m_nRoomIDEnd = self.m_nRoomIDBegin - 1
        self.m_dictRoomID2RoomObj = {}
        self.m_dictGas2RoomNum = {}

    def OnRoomDismiss(self, szGasID, nRoomID):
        self.m_dictRoomID2RoomObj.pop(nRoomID)
        self.m_dictGas2RoomNum[szGasID] -= 1

    def AutoSelectRoom(self):
        for nRoomID, roomObj in self.m_dictRoomID2RoomObj.iteritems():
            if roomObj.IsRunning() is True:
                continue
            return nRoomID, roomObj.GetGasID()

    def Gas2GccGetRoomSceneByRoomID(self, szGasID, nPlayerGID, nRoomID):
        if 0 == nRoomID:
            listRet = self.AutoSelectRoom()
            if listRet is None:
                return
            nRoomID, szRoomInGas = listRet
        else:
            roomObj = self.m_dictRoomID2RoomObj.get(nRoomID)
            if roomObj is not None:
                szRoomInGas = roomObj.GetGasID()
            else:
                szRoomInGas = None

        if szRoomInGas is None:
            return

        ffext.call_service(szGasID, rpc_def.Gcc2GasRetGetRoomScene, {"player_id": nPlayerGID,
                                                                     "gas_id": szRoomInGas,
                                                                     "room_id": nRoomID})

    def Gas2GccGenRoomID(self, szGasID, nPlayerGID, dictCfg):
        if self.m_nRoomIDBegin > self.m_nRoomIDEnd:
            import id_manager.room_id_mgr as room_id_mgr
            self.m_nRoomIDBegin, self.m_nRoomIDEnd = room_id_mgr.GenRoomIDSector()

        nRoomId = self.m_nRoomIDBegin
        self.m_nRoomIDBegin += 1

        gccRoomObj = gcc_room_obj.GccRoomObj()
        gccRoomObj.SetGasID(szGasID)
        self.m_dictRoomID2RoomObj[nRoomId] = gccRoomObj
        self.m_dictGas2RoomNum[szGasID] = self.m_dictGas2RoomNum.get(szGasID, 0) + 1
        ffext.call_service(szGasID, rpc_def.Gcc2GasRetGenRoomID, {"room_id": nRoomId,
                                                                  "player_id": nPlayerGID,
                                                                  "cfg": dictCfg})

    def ChangeRoomStateRunning(self, nRoomID):
        roomObj = self.m_dictRoomID2RoomObj.get(nRoomID)
        assert roomObj is not None
        roomObj.SetIsRunning()

    def OnPlayerExit(self, nPlayerGID):
        pass

    def OnPlayerEnter(self, nPlayerGID):
        pass

_gccRoomMgr = GccRoomMgr()
OnPlayerExit = _gccRoomMgr.OnPlayerExit
OnPlayerEnter = _gccRoomMgr.OnPlayerEnter


@ffext.reg_service(rpc_def.Gas2GccOnRoomDismiss)
def Gas2GccOnRoomDismiss(dictData):
    nRoomID = dictData["room_id"]
    szGasID = dictData["gas_id"]
    _gccRoomMgr.OnRoomDismiss(szGasID, nRoomID)

@ffext.reg_service(rpc_def.Gas2GccGetRoomSceneByRoomID)
def Gas2GccGetRoomSceneByRoomID(dictData):
    szGasID = dictData["gas_id"]
    nPlayerGID = dictData["player_id"]
    nRoomID = dictData["room_id"]
    _gccRoomMgr.Gas2GccGetRoomSceneByRoomID(szGasID, nPlayerGID, nRoomID)

@ffext.reg_service(rpc_def.Gas2GccGenRoomID)
def Gas2GccGenRoomID(dictData):
    szGasID = dictData["gas_id"]
    nPlayerGID = dictData["player_id"]
    dictCfg = dictData["cfg"]
    _gccRoomMgr.Gas2GccGenRoomID(szGasID, nPlayerGID, dictCfg)

@ffext.reg_service(rpc_def.Gas2GccStartGameOnRoom)
def Gas2GccStartGameOnRoom(dictData):
    nRoomID = dictData["room_id"]
    _gccRoomMgr.ChangeRoomStateRunning(nRoomID)