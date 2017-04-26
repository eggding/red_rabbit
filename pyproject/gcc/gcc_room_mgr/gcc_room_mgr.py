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

    def OnRoomDismiss(self, nRoomID):
        self.m_dictRoomID2RoomObj.pop(nRoomID)

    def AutoSelectRoom(self):
        for nRoomID, roomObj in self.m_dictRoomID2RoomObj.iteritems():
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

    def OnGetRoomIdSectorCB(self, dictDbRet, listData):
        if self.m_nRoomIDBegin > self.m_nRoomIDEnd:
            nBegin, nEnd = dictDbRet[dbs_def.RESULT]
            self.m_nRoomIDBegin = nBegin
            self.m_nRoomIDEnd = nEnd
        self.Gas2GccGenRoomID(*listData)

    def Gas2GccGenRoomID(self, szGasID, nPlayerGID):
        if self.m_nRoomIDBegin > self.m_nRoomIDEnd:
            dbs_client.DoAsynCall(rpc_def.DbsGetRoomIDSector, 0, 0, funCb=self.OnGetRoomIdSectorCB, callbackParams=[szGasID, nPlayerGID])
            return

        nRoomId = self.m_nRoomIDBegin
        self.m_nRoomIDBegin += 1

        gccRoomObj = gcc_room_obj.GccRoomObj()
        gccRoomObj.SetGasID(szGasID)
        self.m_dictRoomID2RoomObj[nRoomId] = gccRoomObj
        ffext.call_service(szGasID, rpc_def.Gcc2GasRetGenRoomID, {"room_id": nRoomId,
                                                                  "player_id": nPlayerGID})

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
    _gccRoomMgr.OnRoomDismiss(nRoomID)

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
    _gccRoomMgr.Gas2GccGenRoomID(szGasID, nPlayerGID)