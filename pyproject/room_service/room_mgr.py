# coding=UTF-8

import ff, ffext
import json
import entity.entity_mgr as entity_mgr
import rpc.rpc_def as rpc_def
from rpc.rpc_property_def import RpcProperty
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
        self.m_szGameLogicScene = None
        self.m_nRoomID = nRoomID
        self.m_nMaster = nMaster
        self.m_dictMember = {nMaster: {RoomMemberProperty.ePos: 1,
                                       RoomMemberProperty.eStatus: EStatusInRoom.eReady}} # member -> [nPos, status]

        # 初始化状态机
        self.m_sm = state_machine.StateMachine()
        self.m_sm.ChangeState(room_state_waiting.RoomStateWaiting(self))

    def SetGameLogicScene(self, szScene):
        self.m_szGameLogicScene = szScene

    def GetGameLogicScene(self):
        return self.m_szGameLogicScene

    def GetRoomID(self):
        return self.m_nRoomID

    def Serial(self):
        dictSerial = {
            "id": self.m_nRoomID,
            "member": self.m_dictMember.keys(),
            "master": self.m_nMaster,
        }
        return dictSerial

    def CanStartGame(self):
        if self.m_sm.IsInState(room_state_running.RoomStateRunning) is True:
            return False

        return len(self.m_dictMember) == self.m_nMaxMember

    def StartGameOnRoom(self, szLogicScene):
        self.SetGameLogicScene(szLogicScene)
        self.m_sm.ChangeState(room_state_running.RoomStateRunning(self))
        for nPlayerGID in self.m_dictMember.iterkeys():
            ffext.LOGINFO("FFSCENE_PYTHON", "StartGameOnRoom {0} request change scene {1}".format(nPlayerGID, szLogicScene))
            Player = entity_mgr.GetEntity(nPlayerGID)
            dictSerial = Player.Serial2Dict()
            dictSerial["room_id"] = self.m_nRoomID
            ffext.change_session_scene(nPlayerGID, szLogicScene, json.dumps(dictSerial))

    def MemberEnter(self, nMember):
        self.m_sm.GetCurState().MemberEnter(nMember)

    def MemberExit(self, nMember):
        self.m_sm.GetCurState().MemberExit(nMember)

    def MemberOffline(self, nMember):
        self.m_sm.GetCurState().MemberOffline(nMember)

    def Dismiss(self):
        _roomMgr.OnRoomDismiss(self.GetRoomID(), self.m_dictMember.keys())
        self.Destroy()

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
        self.m_nRoomIDEnd = self.m_nRoomIDBegin - 1

        self.m_dictRoomID2Room = {}
        self.m_dictSession2RoomID = {}
        self.m_residualMgr = residual_mgr.ResidualMgr(self)

    def OnRoomDismiss(self, nRoomID, listRoomPlayers):
        self.m_dictRoomID2Room.pop(nRoomID)
        for nPlayerGID in listRoomPlayers:
            self.m_dictSession2RoomID.pop(nPlayerGID)

    def GetRoomObjByPlayerGID(self, nPlayerGID):
        nRoomID = self.m_dictSession2RoomID.get(nPlayerGID)
        if nRoomID is None:
            return None
        roomObj = self.m_dictRoomID2Room[nRoomID]
        return roomObj

    def RandomChooseRoom(self):
        nRoomID = self.SelectRoom()
        if nRoomID is None:
            return None
        return self.m_dictRoomID2Room[nRoomID]

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
            roomObj.MemberEnter(nPlayerGID)
            return

        if nRoomID is None:
            roomObj = self.RandomChooseRoom()
            if roomObj is None:
                return
        else:
            roomObj = self.m_dictRoomID2Room[nRoomID]

        roomObj.MemberEnter(nPlayerGID)
        self.m_dictSession2RoomID[nPlayerGID] = roomObj.GetRoomID()

        # syn room info 2 client

    def ExitRoom(self, nPlayerGID):
        if nPlayerGID not in self.m_dictSession2RoomID:
            return

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
        ffext.LOGINFO("FFSCENE_PYTHON", "CreateRoom {0}, {1}".format(nRoomMaster, nRoomId))

    def ChooseServiceScene(self):
        return "mj_service@0"

    def OnLogicSceneCreateRoomCb(self, err_, dictRet):
        print(err_)
        ffext.LOGINFO("FFSCENE_PYTHON", "RoomMgr.OnLogicSceneCreateRoomCb {0}".format(json.dumps(dictRet)))
        dictRet = dictRet[RpcProperty.ret]
        nRoomID = dictRet["id"]
        roomObj = self.m_dictRoomID2Room[nRoomID]
        assert roomObj is not None
        roomObj.StartGameOnRoom(dictRet["scene"])

    def StartGame(self, nRoomMaster):
        """
        开局入口
        :param nRoomMaster:
        :return:
        """
        roomObj = self.GetRoomObjByPlayerGID(nRoomMaster)
        if roomObj is None:
            return

        if roomObj.CanStartGame() is False:
            return

        ffext.call_service(self.ChooseServiceScene(), rpc_def.Room2MjStartGame, roomObj.Serial(), self.OnLogicSceneCreateRoomCb)
        ffext.LOGINFO("FFSCENE_PYTHON", "RoomMgr.StartGame {0}".format(nRoomMaster))

    def OnGameEnd(self, nRoomId):
        roomObj = self.m_dictRoomID2Room[nRoomId]
        assert roomObj is not None
        roomObj.Dismiss()

    def OnEnterScene(self, roomPlayer):
        """
        进入场景
        :param roomPlayer:
        :return:
        """
        ffext.LOGINFO("FFSCENE_PYTHON", " OnEnterScene {0}".format(roomPlayer.GetGlobalID()))
        assert roomPlayer is not None

    def OnLeaveScene(self, nPlayerGID):
        """
        离开场景
        :param nPlayerGID:
        :return:
        """
        ffext.LOGINFO("FFSCENE_PYTHON", "OnPlayerLeaveScene {0}".format(nPlayerGID))

        # 加入残留
        self.m_residualMgr.AddResidualPlayer(nPlayerGID)

        # 通知成员
        roomObj = self.GetRoomObjByPlayerGID(nPlayerGID)
        if roomObj is not None:
            roomObj.MemberExit(nPlayerGID)

    def PlayerTrueOffline(self, nPlayerGID):
        """
        下线
        :param nPlayerGID:
        :return:
        """
        ffext.LOGINFO("FFSCENE_PYTHON", "player true offline {0}".format(nPlayerGID))
        Player = entity_mgr.GetEntity(nPlayerGID)
        if Player is not None:
            Player.Destroy()
        entity_mgr.DelEntity(nPlayerGID)

        self.ExitRoom(nPlayerGID)

_roomMgr = RoomService()
OnPlayerLeaveScene = _roomMgr.OnLeaveScene
OnGameEnd = _roomMgr.OnGameEnd

def OnLoadPlayerDataDone(dictSerialData, dictExtra):
    assert dictSerialData[dbs_def.FLAG] is True
    util.dict_merge(json.loads(dictExtra), dictSerialData)

    ffext.LOGINFO("FFSCENE_PYTHON", "OnLoadPlayerDataDone {0}".format(json.dumps(dictSerialData)))
    roomPlayer = player_in_room_service.RoomPlayer()
    roomPlayer.InitFromDict(dictSerialData)
    entity_mgr.AddEntity(roomPlayer.GetGlobalID(), roomPlayer)

    _roomMgr.OnEnterScene(roomPlayer)

    import proto.login_pb2 as login_pb2
    syn_scene = login_pb2.syn_enter_scene()
    syn_scene.ret = 0
    syn_scene.scene_id = 1
    syn_scene.scene_info = ff.service_name
    # ffext.send_msg_session(roomPlayer.GetSession(), rpc_def.SynSceneInfo, syn_scene.SerializeToString())
    # ffext.send_msg_session(roomPlayer.GetSession(), rpc_def.SynPlayerData, roomPlayer.Serial2Client())

@ffext.session_enter_callback
def OnSessionEnterScene(nPlayerGID, szSrcScene, dictSerialData):
    ffext.LOGINFO("FFSCENE_PYTHON", "enter room center {0}".format(nPlayerGID))
    if szSrcScene == scene_def.LOGIN_SCENE:
        if _roomMgr.m_residualMgr.IsPlayerInResidual(nPlayerGID) is True:
            _roomMgr.m_residualMgr.RemoveResidualPlayer(nPlayerGID)
            _roomMgr.OnEnterScene(entity_mgr.GetEntity(nPlayerGID))
        else:
            # load from dbs
            dbs_client.DoAsynCall(rpc_def.DbsLoadPlayerData, nPlayerGID, 0, nChannel=nPlayerGID, funCb=OnLoadPlayerDataDone, callbackParams=dictSerialData)


