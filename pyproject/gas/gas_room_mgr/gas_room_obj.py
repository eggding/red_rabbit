# -*- coding: utf-8 -*-
# @Author  : jh.feng

import ff, ffext
import entity.entity_mgr as entity_mgr
from util.enum_def import RoomMemberProperty, EGameRule, EMemberEvent, EMoneyType, EStatusInRoom
import state.state_machine as state_machine
import state.room_state_waiting as room_state_waiting
import state.room_state_running as room_state_running
import gas.gas_game_rule.game_rule_mgr as game_rule_mgr
import rpc.scene_def as scene_def
import rpc.rpc_def as rpc_def
import cfg_py.parameter_common as parameter_common

class RoomObj(object):
    def __init__(self, nRoomID, nMaster, roomMgr, dictConfig):
        self.m_nMaxMember = dictConfig.get("member_num", 4)
        self.m_roomMgr = roomMgr
        self.m_nRoomID = nRoomID
        self.m_nMaster = nMaster
        self.m_dictMember = {} # member -> [nPos, status]

        self.m_dictCfg = dictConfig
        self.m_bIsFirstStart = True

        # 初始化状态机
        self.m_sm = state_machine.StateMachine()
        self.m_sm.ChangeState(room_state_waiting.RoomStateWaiting(self))

        self.m_gameRuleObj = game_rule_mgr.GetGameRule(EGameRule.eGameRuleMj)(self)
        self.MemberEnter(nMaster)

    def GameRuleOpt(self, nPlayerGID, reqObj):
        self.m_gameRuleObj.GacOpt(nPlayerGID, reqObj)

    def GetConfig(self):
        return self.m_dictCfg

    def GetMemberByPos(self, nPos):
        for nMember, listData in self.m_dictMember.iteritems():
            nCurPos = listData[RoomMemberProperty.ePos]
            if nCurPos != nPos:
                continue
            return nMember

    def GetCreateRoomNeedMoney(self):
        return parameter_common.parameter_common[3]["参数"]

    def GetMemberNum(self):
        return len(self.m_dictMember)

    def GetMemberPos(self, nMember):
        return self.m_dictMember[nMember][RoomMemberProperty.ePos]

    def GetMemberState(self, nMember):
        return self.m_dictMember[nMember][RoomMemberProperty.eStatus]

    def GetMemberIDByPos(self, nPos):
        for nMemberGID, dictData in self.m_dictMember.iteritems():
            if dictData[RoomMemberProperty.ePos] == nPos:
                return nMemberGID
        assert False

    def IsRunning(self):
        return self.m_sm.IsInState(room_state_running.RoomStateRunning)

    def GetMemberList(self):
        return self.m_dictMember.keys()

    def GetRoomID(self):
        return self.m_nRoomID

    def OnGameEnd(self):
        self.Dismiss()

    def SynMemberState2All(self, nMemberID, nState):
        import proto.common_info_pb2 as common_info_pb2
        rsp = common_info_pb2.syn_member_state_rsp()
        rsp.ret = 0
        rsp.room_id = self.GetRoomID()
        rsp.member_info.pos = self.GetMemberPos(nMemberID)
        rsp.member_info.state = nState

        Player = entity_mgr.GetEntity(nMemberID)
        assert Player is not None
        Player.Serial2Client(rsp.member_info)

        for nMember in self.m_dictMember.iterkeys():
            if nMemberID == nMember:
                continue
            ffext.send_msg_session(nMember, rpc_def.Gas2GacRetSynMemberState, rsp.SerializeToString())

    def SynGameInfo(self, nPlayerGID, bSynAll=False):
        import proto.common_info_pb2 as common_info_pb2
        rsp = common_info_pb2.syn_game_info()
        rsp.room_id = self.GetRoomID()
        rsp.cur_game_num = 0 #
        rsp.cur_round = self.m_gameRuleObj.GetCurJu()
        rsp.cur_turn = self.m_gameRuleObj.GetCurTurn()
        rsp.remain_card_num = self.m_gameRuleObj.GetCardRemain()
        rsp.room_state = EStatusInRoom.eWaiting if self.m_sm.IsInState(room_state_running.RoomStateRunning) is False else EStatusInRoom.eRunning

        nZhuang = self.m_gameRuleObj.GetZhuang()
        rsp.master_id = nZhuang if nZhuang == 0 else self.GetMemberPos(nZhuang)

        listJinPai = self.m_gameRuleObj.GetJinPaiList()
        for nJin in listJinPai:
            rsp.list_gold_card.append(nJin)

        rsp.pos_owner = self.GetMemberPos(nPlayerGID)
        rsp.opt_pos = self.m_gameRuleObj.GetCurOptMemberPos()

        for nMember, listVal in self.m_dictMember.iteritems():
            nPos = listVal[RoomMemberProperty.ePos]
            tmp = rsp.card_info.add()
            self.m_gameRuleObj.InitCardInfoByPos(nPos, tmp, True if nPlayerGID == nMember else False)

        if bSynAll is True:
            for nMember in self.m_dictMember.iterkeys():
                if nMember == nPlayerGID:
                    continue
                tmp = rsp.list_members.add()
                tmp.pos = self.GetMemberPos(nMember)
                tmp.state = self.GetMemberState(nMember)
                Player = entity_mgr.GetEntity(nMember)
                assert Player is not None
                Player.Serial2Client(tmp)

        ffext.send_msg_session(nPlayerGID, rpc_def.Gas2GacRspSynGameData, rsp.SerializeToString())

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

        if len(self.m_dictMember) != self.m_nMaxMember:
            return False

        for nMember, listData in self.m_dictMember.iteritems():
            nFlag = listData[RoomMemberProperty.eStatus]
            if nFlag != EStatusInRoom.eReady:
                return False

        return True

    def ChangeRoomStateToWaiting(self):
        import util.util as util
        for nMember, listData in self.m_dictMember.iteritems():
            if util.IsRobot(nMember) is True:
                listData[RoomMemberProperty.eStatus] = EStatusInRoom.eReady
            else:
                listData[RoomMemberProperty.eStatus] = EStatusInRoom.eUnReady
        self.m_sm.ChangeState(room_state_waiting.RoomStateWaiting(self))

    def StartGameOnRoom(self):
        ffext.LOGINFO("FFSCENE_PYTHON", "StartGameOnRoom {0}".format(self.GetRoomID()))

        if self.m_bIsFirstStart is True:
            bIsAvg = True if self.GetConfig()["avg"] != 0 else False
            if bIsAvg is True:
                nRoomMasterDel = self.GetCreateRoomNeedMoney() / self.GetConfig()["member_num"]
                assert nRoomMasterDel > 0
                nRoomOtherDel = nRoomMasterDel
            else:
                nRoomMasterDel = self.GetCreateRoomNeedMoney()
                nRoomOtherDel = 0

            for nMember in self.m_dictMember.iterkeys():
                Player = entity_mgr.GetEntity(nMember)
                if nMember == self.m_nMaster:
                    nDelNum = nRoomMasterDel
                else:
                    nDelNum = nRoomOtherDel
                # if Player.IsMoneyEnough(EMoneyType.eZhuanShi, nDelNum) is False:
                #     return

            for nMember in self.m_dictMember.iterkeys():
                Player = entity_mgr.GetEntity(nMember)
                if nMember == self.m_nMaster:
                    nDelNum = nRoomMasterDel
                else:
                    nDelNum = nRoomOtherDel
                if nDelNum != 0:
                    pass
                    # if Player.AddMoney(EMoneyType.eZhuanShi, -nDelNum, "开场扣除") is False:
                    #     return

            self.m_sm.ChangeState(room_state_running.RoomStateRunning(self))
            for nMember in self.m_dictMember.iterkeys():
                Player = entity_mgr.GetEntity(nMember)
                Player.SetRoomID(self.GetRoomID())
        else:
            self.m_bIsFirstStart = False

        self.m_gameRuleObj.GameStart()
        ffext.call_service(scene_def.GCC_SCENE, rpc_def.Gas2GccStartGameOnRoom, {"room_id": self.GetRoomID()})

    def GetGameRule(self):
        return self.m_gameRuleObj

    def NoticeMsg(self, msg, msgData):
        pass

    def NoticeMemberEvent(self, ev, nModMember):
        # notice other members
        import rpc.rpc_def as rpc_def
        import proto.common_info_pb2 as common_info_pb2
        rsp = common_info_pb2.on_touch_event_member()
        rsp.ev_type = ev

        inf = rsp.list_member.add()
        inf.pos = self.GetMemberPos(nModMember)
        Player = entity_mgr.GetEntity(nModMember)
        Player.Serial2Client(inf)

        for nMemberOther, dictData in self.m_dictMember.iteritems():
            if nMemberOther == nModMember:
                continue
            print("ffext.send_msg_session ", nMemberOther)
            ffext.send_msg_session(nMemberOther, rpc_def.Gas2GacOnTouchMemberEvent, rsp.SerializeToString())

    def MemberEnter(self, nMember):
        bRet = self.m_sm.GetCurState().MemberEnter(nMember)
        if bRet is True:
            self.NoticeMemberEvent(EMemberEvent.evMemberEnter, nMember)

    def MemberReady(self, nMember):
        self.m_sm.GetCurState().MemberReady(nMember)

    def MemberExit(self, nMember):
        self.NoticeMemberEvent(EMemberEvent.evMemberExit, nMember)
        self.m_sm.GetCurState().MemberExit(nMember)

    def MemberOffline(self, nMember):
        self.NoticeMemberEvent(EMemberEvent.evMemberExit, nMember)
        self.m_sm.GetCurState().MemberOffline(nMember)

    def Dismiss(self):
        self.m_roomMgr.OnRoomDismiss(self.GetRoomID(), self.m_dictMember.keys())
        self.m_dictMember = {}
        self.m_bIsFirstStart = True
        self.Destroy()

    def Destroy(self):
        self.m_sm.Destroy()
        self.m_roomMgr = None

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

