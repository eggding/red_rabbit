# coding=UTF-8

import ff, ffext
import json
import entity.entity_mgr as entity_mgr
import rpc.rpc_def as rpc_def
import entity.player_in_room_service as player_in_room_service
import rpc.scene_def as scene_def
import db.dbs_client as dbs_client
import db.dbs_def as dbs_def
import util.util as util
from util.enum_def import EStatusInRoom, RoomMemberProperty
import residual.residual_mgr as residual_mgr
import state.state_machine as state_machine
import state.room_state_waiting as room_state_waiting
import state.room_state_running as room_state_running

class RoomObj(object):
    def __init__(self, nRoomID,  nMaster):
        self.m_nMaxMember = 4
        self.m_szRoomInScene = None
        self.m_nRoomID = nRoomID
        self.m_nMaster = nMaster
        self.m_dictMember = {nMaster: {RoomMemberProperty.ePos: 1,
                                       RoomMemberProperty.eStatus: EStatusInRoom.eReady}} # member -> [nPos, status]

        # 初始化状态机
        self.m_sm = state_machine.StateMachine()
        self.m_sm.ChangeState(room_state_waiting.RoomStateWaiting(self))

    def StartGameOnRoom(self):
        self.m_sm.ChangeState(room_state_running.RoomStateRunning(self))

    def MemberEnter(self, nMember):
        self.m_sm.MemberEnter(nMember)

    def MemberExit(self, nMember):
        self.m_sm.MemberExit(nMember)

    def MemberOffline(self, nMember):
        self.m_sm.MemberOffline(nMember)

    def Destroy(self):
        self.m_sm.Destroy()

    def GetEmptyPos(self):
        return self.m_nMaxMember - len(self.m_dictMember)

    def GenPos(self):
        for nPos in xrange(1, self.m_nMaxMember + 1):
            bExist = False
            for dictData in self.m_dictMember.itervalues():
                nHavePos = dictData[RoomMemberProperty.ePos]
                if nHavePos == nPos:
                    bExist = True
                    break
            if bExist is False:
                return nPos
        assert False


class RoomService(object):
    def __init__(self):
        self.m_nRoomIDBegin = 0
        self.m_nRoomIDEnd = self.m_nRoomIDBegin

        self.m_dictRoomID2Room = {}
        self.m_dictSession2RoomID = {}
        self.m_residualMgr = residual_mgr.ResidualMgr(self)

    def GetRoomObjByPlayerGID(self, nPlayerGID):
        nRoomID = self.m_dictSession2RoomID.get(nPlayerGID)
        if nRoomID is None:
            return None
        roomObj = self.m_dictRoomID2Room[nRoomID]
        return roomObj

    def SelectRoom(self):
        nDstRoomID = None
        nEmptyPos = None
        for nRoomID, roomObj in self.m_dictRoomID2Room.iteritems():
            nHavePosNum = roomObj.GetEmptyPos()
            if 0 == nHavePosNum:
                continue

            if nDstRoomID is None:
                nDstRoomID = nRoomID
                nEmptyPos = nHavePosNum
                continue

            if nEmptyPos > nHavePosNum:
                nEmptyPos = nHavePosNum
                nDstRoomID = nRoomID

        return nDstRoomID

    def EnterRoom(self, nPlayerGID, nRoomID=None):
        # 已经有room
        roomObj = self.GetRoomObjByPlayerGID(nPlayerGID)
        if roomObj is not None:
            pass
        else:
            if nRoomID is None:
                nRoomID = self.SelectRoom()
            if nRoomID is None:
                return
            roomObj = self.m_dictRoomID2Room[nRoomID]
            roomObj.AddMember(nPlayerGID)
            self.m_dictSession2RoomID[nPlayerGID] = nRoomID

        # syn room info 2 client

    def ExitRoom(self, nPlayerGID):
        self.m_dictSession2RoomID.pop(nPlayerGID)
        roomObj = self.GetRoomObjByPlayerGID(nPlayerGID)
        if roomObj is not None:
            roomObj.MemberExit(nPlayerGID)

    def OnGetRoomIdSectorCB(self, dictDbRet, listData):
        if self.m_nRoomIDBegin > self.m_nRoomIDEnd:
            nBegin, nEnd = dictDbRet[dbs_def.RESULT]
            self.m_nRoomIDBegin = nBegin
            self.m_nRoomIDEnd = nEnd
        self.CreateRoom(*listData)

    def CreateRoom(self, nRoomMaster, data):
        if self.m_nRoomIDBegin > self.m_nRoomIDEnd:
            dbs_client.DoAsynCall(rpc_def.DbsGetRoomIDSector, 0, 0, funCb=self.OnGetRoomIdSectorCB, callbackParams=[nRoomMaster, data])
            return

        nRoomId = self.m_nRoomIDBegin
        self.m_nRoomIDBegin += 1
        roomObj = RoomObj(nRoomId, nRoomMaster)
        self.m_dictRoomID2Room[nRoomId] = roomObj
        self.m_dictSession2RoomID[nRoomMaster] = nRoomId

        # to gac.

    def OnPlayerEnterScene(self, roomPlayer):
        entity_mgr.AddEntity(roomPlayer.GetSession(), roomPlayer)

    def OnPlayerLeaveScene(self, session):
        roomObj = self.GetRoomObjByPlayerGID(session)
        if roomObj is not None:
            roomObj.MemberOffline(session)

        Player = entity_mgr.GetEntity(session)
        if Player is not None:
            Player.Destroy()
        entity_mgr.DelEntity(session)

_roomMgr = RoomService()
OnPlayerLeaveScene = _roomMgr.OnPlayerLeaveScene

def OnLoadPlayerDataDone(dictSerialData, dictExtra):
    assert dictSerialData[dbs_def.FLAG] is True
    util.dict_merge(json.loads(dictExtra), dictSerialData)

    ffext.LOGINFO("FFSCENE_PYTHON", "OnLoadPlayerDataDone {0}".format(json.dumps(dictSerialData)))
    roomPlayer = player_in_room_service.RoomPlayer()
    roomPlayer.InitFromDict(dictSerialData)
    _roomMgr.OnPlayerEnterScene(roomPlayer)

    import proto.login_pb2 as login_pb2
    syn_scene = login_pb2.syn_enter_scene()
    syn_scene.ret = 0
    syn_scene.scene_id = 1
    syn_scene.scene_info = ff.service_name
    # ffext.send_msg_session(roomPlayer.GetSession(), rpc_def.SynSceneInfo, syn_scene.SerializeToString())
    # ffext.send_msg_session(roomPlayer.GetSession(), rpc_def.SynPlayerData, roomPlayer.Serial2Client())

def OnPlayerEnterScene(nPlayerGID, szSrcScene, dictSerialData):
    # print("OnPlayerEnterScene room  ", nPlayerGID, dictSerialData)
    ffext.LOGINFO("FFSCENE_PYTHON", "enter room center {0}".format(nPlayerGID))
    if szSrcScene == scene_def.LOGIN_SCENE:
        dbs_client.DoAsynCall(rpc_def.DbsLoadPlayerData, nPlayerGID, 0, nChannel=nPlayerGID, funCb=OnLoadPlayerDataDone, callbackParams=dictSerialData)
    else:
        OnLoadPlayerDataDone(dictSerialData, "{}")

ffext.g_session_enter_callback = OnPlayerEnterScene


