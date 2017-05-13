# -*- coding: utf-8 -*-
# @Author  : jh.feng

import ff, ffext
import entity.entity_mgr as entity_mgr
from util.enum_def import RoomMemberProperty, EGameRule, EMemberEvent, EMoneyType
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

        # 初始化状态机
        self.m_sm = state_machine.StateMachine()
        self.m_sm.ChangeState(room_state_waiting.RoomStateWaiting(self))

        self.m_gameRuleObj = game_rule_mgr.GetGameRule(EGameRule.eGameRuleMj)(self)
        self.MemberEnter(nMaster)

    def GameRuleOpt(self, nPlayerGID, reqObj):
        self.m_gameRuleObj.GacOpt(nPlayerGID, reqObj)

    def GetConfig(self):
        return self.m_dictCfg

    def GetCreateRoomNeedMoney(self):
        return parameter_common.parameter_common[3]["参数"]

    def GetMemberNum(self):
        return len(self.m_dictMember)

    def GetMemberPos(self, nMember):
        return self.m_dictMember[nMember][RoomMemberProperty.ePos]

    def GetMemberIDByPos(self, nPos):
        for nMemberGID, dictData in self.m_dictMember.iteritems():
            if dictData[RoomMemberProperty.ePos] == nPos:
                return nMemberGID
        assert False

    def GetMemberList(self):
        return self.m_dictMember.keys()

    def GetRoomID(self):
        return self.m_nRoomID

    def OnGameEnd(self):
        self.Dismiss()

    def SynGameInfo(self, nPlayerGID, bIsGameRunning):
        nPos = self.GetMemberPos(nPlayerGID)

        import rpc.rpc_def as rpc_def
        import proto.common_info_pb2 as common_info_pb2
        rsp = common_info_pb2.syn_game_info()
        rsp.room_id = self.GetRoomID()
        rsp.cfg.member_num = 0
        rsp.cfg.multi = 0
        rsp.cfg.total_start_game_num = 0
        # rsp.cfg.avg = 0
        rsp.cfg.opt = 1

        # required uint32         member_num = 1; // 开局人数
        # required uint32         multi = 2; // 游金倍数
        # required uint32         total_start_game_num = 3; // 总场数
        # required uint32         avg = 4; // 是否均摊
        # required room_option    opt = 5; // 玩法选项


        rsp.cur_game_num = 0
        rsp.cur_round = self.m_gameRuleObj.GetCurJu()
        rsp.cur_turn = 0
        rsp.remain_card_num = self.m_gameRuleObj.GetCardRemain()
        rsp.master_id = self.m_gameRuleObj.GetZhuang()

        for nGoldCard in self.m_gameRuleObj.GetJinPaiList():
            tmpObj = rsp.list_gold_card.add()
            tmpObj = nGoldCard

        for nCard in self.m_gameRuleObj.GetPosCardList(nPos):
            tmpObj = rsp.list_owner_card.add()
            tmpObj = nCard

        import entity.entity_mgr as entity_mgr
        listMembers = self.GetMemberList()
        for nMember in listMembers:
            inf = rsp.list_members.add()
            inf.pos = self.GetMemberPos(nMember)
            Player = entity_mgr.GetEntity(nMember)
            Player.Serial2Client(inf)

        print("syn game info ", nPlayerGID)

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

        return len(self.m_dictMember) == self.m_nMaxMember

    def StartGameOnRoom(self):
        ffext.LOGINFO("FFSCENE_PYTHON", "StartGameOnRoom {0}".format(self.GetRoomID()))
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
            if Player.IsMoneyEnough(EMoneyType.eZhuanShi, nDelNum) is False:
                return

        for nMember in self.m_dictMember.iterkeys():
            Player = entity_mgr.GetEntity(nMember)
            if nMember == self.m_nMaster:
                nDelNum = nRoomMasterDel
            else:
                nDelNum = nRoomOtherDel
            if nDelNum != 0:
                if Player.AddMoney(EMoneyType.eZhuanShi, -nDelNum, "开场扣除") is False:
                    return

        self.m_sm.ChangeState(room_state_running.RoomStateRunning(self))
        for nMember in self.m_dictMember.iterkeys():
            Player = entity_mgr.GetEntity(nMember)
            Player.SetRoomID(self.GetRoomID())

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
            ffext.send_msg_session(nMemberOther, rpc_def.Gas2GacOnTouchMemberEvent, rsp.SerializeToString())

    def MemberEnter(self, nMember):
        bRet = self.m_sm.GetCurState().MemberEnter(nMember)
        if bRet is True:
            self.NoticeMemberEvent(EMemberEvent.evMemberEnter, nMember)

    def MemberExit(self, nMember):
        self.NoticeMemberEvent(EMemberEvent.evMemberExit, nMember)
        self.m_sm.GetCurState().MemberExit(nMember)

    def MemberOffline(self, nMember):
        self.NoticeMemberEvent(EMemberEvent.evMemberExit, nMember)
        self.m_sm.GetCurState().MemberOffline(nMember)

    def Dismiss(self):
        self.m_roomMgr.OnRoomDismiss(self.GetRoomID(), self.m_dictMember.keys())
        self.m_dictMember = {}
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

