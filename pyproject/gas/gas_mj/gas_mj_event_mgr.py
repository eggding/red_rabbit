# -*- coding: utf-8 -*-
# @Author  : jh.feng

import json
import ffext as framework
import proto.common_info_pb2 as common_info_pb2
from util.enum_def import EMjEvent, ECardType
import rpc.rpc_def as rpc_def
import util.tick_mgr as tick_mgr
import check_hu as check_hu_mgr

class MjEventObj(object):
    def __init__(self, evType, nTarget, szData, nSrcTarget=0):
        self.m_nEventType = evType
        self.m_nTarget = nTarget
        self.m_nSrcTarget = nSrcTarget
        self.m_szEventData = szData

    def Serial2Client(self, inf):
        inf.ev_type = self.m_nEventType
        inf.ev_target = self.m_nTarget
        inf.ev_data = self.m_szEventData
        inf.ev_target_src = self.m_nSrcTarget

class GasMjEventMgr(object):
    def __init__(self):
        self.m_dictEventType2Opt = {EMjEvent.ev_bu_hua: self.EventBuHua,
                                    EMjEvent.ev_mo_pai: self.TouchEventMoPai,
                                    EMjEvent.ev_be_qi_pai: self.TouchEventQiPai,
                                    EMjEvent.ev_kai_jin: self.TouchEventKaiJin,
                                    EMjEvent.ev_peng: self.TouchEventPeng,
                                    EMjEvent.ev_gang_with_peng: self.TouchEventGangWithPeng,
                                    EMjEvent.ev_hu_ba_xian_guo_hai: self.TouchEventBaXianGuoHai,
                                    }

    def TouchEvent(self, mjMgr, ev, evData=None):
        funOpt = self.m_dictEventType2Opt[ev]
        return funOpt(mjMgr, evData)

    def TouchEventPeng(self, mjMgr, listData):
        pass

    def TouchEventKaiJin(self, mjMgr, listJinPai):
        roomObj = mjMgr.GetRoomObj()
        listMember = roomObj.GetMemberList()
        evObj = MjEventObj(EMjEvent.ev_kai_jin, 0, mjMgr.SerialList2Str(listJinPai))
        for nMember in listMember:
            nPos = mjMgr.GetRoomObj().GetMemberPos(nMember)
            mjMgr.AddEventNotic2Poll(nPos, evObj)

    def TouchEventGangWithPeng(self, mjMgr, listData):
        pass

    def TouchEventBaXianGuoHai(self, mjMgr, listData):
        nPos = listData[0]
        roomObj = mjMgr.GetRoomObj()
        nOptMember = roomObj.GetMemberIDByPos(nPos)
        evObj = MjEventObj(EMjEvent.ev_hu_ba_xian_guo_hai, nOptMember, "")
        mjMgr.AddEventNotic2Poll(nPos, evObj)
        framework.LOGINFO("FFSCENE_PYTHON", "GasMj.BaXianGuoHai {0} {1}".format(nPos, mjMgr.DumpPos(nPos)))

    def TouchEventQiPai(self, mjMgr, listData):
        nPos, nCard = listData
        roomObj = mjMgr.GetRoomObj()
        listMember = roomObj.GetMemberList()
        nOptMember = roomObj.GetMemberIDByPos(nPos)

        evObj = MjEventObj(EMjEvent.ev_be_qi_pai, nOptMember, str(nCard))
        for nMember in listMember:
            nMemberPos = roomObj.GetMemberPos(nMember)
            mjMgr.AddEventNotic2Poll(nMemberPos, evObj)
            # framework.send_msg_session(nMember, rpc_def.Gas2GacOnTouchGameEvent, szRspSerial)

        listCardOwner = mjMgr.GetCardListByPos(nPos)
        nTotal = len(listCardOwner)
        assert ((nTotal - 1) % 3 == 0), nTotal

        listJinPai = mjMgr.GetJinPaiList()

        bNextTurn = True
        for nMember in listMember:
            if nMember == nOptMember:
                continue

            nMemberPos = mjMgr.GetRoomObj().GetMemberPos(nMember)
            listCard = mjMgr.GetCardListByPos(nMemberPos)
            listCardEx = mjMgr.GetCardListEx(nMemberPos)

            # check gang, owenr have 3
            if check_hu_mgr.testGang(nCard, listCard, listJinPai) is True:
                evObj = MjEventObj(EMjEvent.ev_gang_other, nOptMember, str(nCard))
                mjMgr.AddEventNotic2Poll(nMemberPos, evObj)
                mjMgr.SetCurEventOptMember(nMember)
                if mjMgr.IsTuoGuan(nMember):
                    tick_mgr.RegisterOnceTick(100, mjMgr.RequestGang, [nMember, nOptMember, nCard])

                framework.LOGINFO("FFSCENE_PYTHON", "GasMj.Gang {0}, {1} ".format(json.dumps(listCard), nCard))
                bNextTurn = False
                continue

            # check gang with peng
            if check_hu_mgr.testGang(nCard, listCardEx, listJinPai) is True:
                evObj = MjEventObj(EMjEvent.ev_gang_with_peng, nOptMember, str(nCard))
                mjMgr.AddEventNotic2Poll(nMemberPos, evObj)
                mjMgr.SetCurEventOptMember(nMember)
                if mjMgr.IsTuoGuan(nMember):
                    tick_mgr.RegisterOnceTick(100, mjMgr.RequestGang, [nMember, nOptMember, nCard])

                framework.LOGINFO("FFSCENE_PYTHON", "GasMj.Gang {0}, {1} ".format(json.dumps(listCard), nCard))
                bNextTurn = False
                continue

            # check peng
            if check_hu_mgr.testPeng(nCard, listCard, listJinPai) is True:
                evObj = MjEventObj(EMjEvent.ev_peng, nOptMember, str(nCard))
                mjMgr.AddEventNotic2Poll(nMemberPos, evObj)
                mjMgr.SetCurEventOptMember(nMember)
                if mjMgr.IsTuoGuan(nMember):
                    tick_mgr.RegisterOnceTick(100, mjMgr.RequestPeng, [nMember, nOptMember, nCard])

                framework.LOGINFO("FFSCENE_PYTHON", "GasMj.Peng {0}, {1} ".format(json.dumps(listCard), nCard))
                bNextTurn = False
                continue

        return bNextTurn

    def TouchEventMoPai(self, mjMgr, listData):
        nPos, nCard = listData
        roomObj = mjMgr.GetRoomObj()
        nOptMember = roomObj.GetMemberIDByPos(nPos)

        nCardType = check_hu_mgr.GetCardType(nCard)
        if nCardType == ECardType.eHuaPai:
            return

        # 摸到这张牌是不是能胡牌
        listCard = mjMgr.GetPosCardList(nPos)
        assert ((len(listCard) - 2) % 3 == 0)

        listJinPai = mjMgr.GetJinPaiList()

        import time
        nTimeCheckPre = time.clock()
        bCanHu = check_hu_mgr.testHu(0, listCard, listJinPai)
        nTimeENd = time.clock()
        framework.LOGINFO("FFSCENE_PYTHON", "GasMj.CheckHU {0} ".format(nTimeENd - nTimeCheckPre))
        if bCanHu is True:
            evObj = MjEventObj(EMjEvent.ev_hu_normal, nOptMember, str(nCard))
            mjMgr.AddEventNotic2Poll(nPos, evObj)
            mjMgr.SetCurEventOptMember(nOptMember)
            if mjMgr.IsTuoGuan(nOptMember) is True:
                tick_mgr.RegisterOnceTick(100, mjMgr.RequestHu, [nOptMember])

            framework.LOGINFO("FFSCENE_PYTHON",
                              "GasMj.CanHu {0}, {1} ".format(json.dumps(listJinPai), json.dumps(mjMgr.DumpPos(nPos))))

        if listCard.count(nCard) == 4:
            evObj = MjEventObj(EMjEvent.ev_gang_all, nOptMember, str(nCard))
            mjMgr.AddEventNotic2Poll(nPos, evObj)
            mjMgr.SetCurEventOptMember(nOptMember)
            if mjMgr.IsTuoGuan(nOptMember):
                tick_mgr.RegisterOnceTick(100, mjMgr.RequestGang, [nOptMember, nOptMember, nCard])

            framework.LOGINFO("FFSCENE_PYTHON", "GasMj.GangAll {0}, {1} ".format(json.dumps(listCard), nCard))

        return True

    def EventBuHua(self, mjMgr, listData):
        nPos, nHuaPai, nCard = listData

        roomObj = mjMgr.GetRoomObj()
        listMember = roomObj.GetMemberList()
        nOptMember = roomObj.GetMemberIDByPos(nPos)

        evObj = MjEventObj(EMjEvent.ev_bu_hua, nOptMember, "{0},{1}".format(nHuaPai, nCard))
        for nMember in listMember:
            nMemberPos = mjMgr.GetRoomObj().GetMemberPos(nMember)
            mjMgr.AddEventNotic2Poll(nMemberPos, evObj)

        return True

_mjEventMgr = GasMjEventMgr()
TouchEvent = _mjEventMgr.TouchEvent
