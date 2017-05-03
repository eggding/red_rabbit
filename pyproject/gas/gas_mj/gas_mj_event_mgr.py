# -*- coding: utf-8 -*-
# @Author  : jh.feng

import json
import ffext as framework
import proto.common_info_pb2 as common_info_pb2
from util.enum_def import EMjEvent, ECardType
import rpc.rpc_def as rpc_def
import util.tick_mgr as tick_mgr
import check_hu as check_hu_mgr

class GasMjEventMgr(object):
    def __init__(self):
        self.m_dictEventType2Opt = {EMjEvent.ev_bu_hua: self.EventBuHua,
                                    EMjEvent.ev_mo_pai: self.TouchEventMoPai,
                                    EMjEvent.ev_qi_pai: self.TouchEventQiPai,
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
        rsp = common_info_pb2.on_touch_event()
        rsp.ev_type = EMjEvent.ev_kai_jin
        rsp.ev_target = 0
        rsp.ev_data = json.dumps(listJinPai)
        szRspSerial = rsp.SerializeToString()
        for nMember in listMember:
            framework.send_msg_session(nMember, rpc_def.Gas2GacOnTouchGameEvent, szRspSerial)

    def TouchEventGangWithPeng(self, mjMgr, listData):
        pass

    def TouchEventBaXianGuoHai(self, mjMgr, listData):
        nPos = listData[0]
        roomObj = mjMgr.GetRoomObj()
        nOptMember = roomObj.GetMemberIDByPos(nPos)
        rsp = common_info_pb2.on_touch_event()
        rsp.ev_type = EMjEvent.ev_hu_ba_xian_guo_hai
        rsp.ev_target = nOptMember
        rsp.ev_data = ""
        szRspSerial = rsp.SerializeToString()
        framework.send_msg_session(nOptMember, rpc_def.Gas2GacOnTouchGameEvent, szRspSerial)
        framework.LOGINFO("FFSCENE_PYTHON", "GasMj.BaXianGuoHai {0} {1}".format(nPos, mjMgr.DumpPos(nPos)))

    def TouchEventQiPai(self, mjMgr, listData):
        nPos, nCard = listData
        roomObj = mjMgr.GetRoomObj()
        listMember = roomObj.GetMemberList()
        nOptMember = roomObj.GetMemberIDByPos(nPos)
        rsp = common_info_pb2.on_touch_event()
        rsp.ev_type = EMjEvent.ev_qi_pai
        rsp.ev_target = nOptMember
        rsp.ev_data = str(nCard)
        szRspSerial = rsp.SerializeToString()
        for nMember in listMember:
            framework.send_msg_session(nMember, rpc_def.Gas2GacOnTouchGameEvent, szRspSerial)

        listCardOwner = mjMgr.GetCardListByPos(nPos)
        nTotal = len(listCardOwner)
        assert ((nTotal - 1) % 3 == 0), nTotal

        listJinPai = mjMgr.GetJinPaiList()
        tingArr = check_hu_mgr.getTingArr(listCardOwner, listJinPai)
        if len(tingArr) != 0:
            rsp = common_info_pb2.on_touch_event()
            rsp.ev_type = EMjEvent.ev_hu_normal
            rsp.ev_target = nOptMember
            rsp.ev_data = json.dumps(tingArr)
            szRspSerial = rsp.SerializeToString()
            framework.send_msg_session(nOptMember, rpc_def.Gas2GacOnTouchGameEvent, szRspSerial)
            framework.LOGINFO("FFSCENE_PYTHON",
                              "GasMj.tingArr {0}, {1}, {2} ".format(nPos, json.dumps(tingArr), mjMgr.DumpPos(nPos)))

        bNextTurn = True
        for nMember in listMember:
            if nMember == nOptMember:
                continue

            nMemberPos = mjMgr.GetRoomObj().GetMemberPos(nMember)
            listCard = mjMgr.GetCardListByPos(nMemberPos)
            listCardEx = mjMgr.GetCardListEx(nMemberPos)

            # check gang, owenr have 3
            if check_hu_mgr.testGang(nCard, listCard, listJinPai) is True:
                rsp.ev_type = EMjEvent.ev_gang_other
                rsp.ev_target = nOptMember
                rsp.ev_data = str(nCard)
                szRspSerial = rsp.SerializeToString()
                framework.send_msg_session(nMember, rpc_def.Gas2GacOnTouchGameEvent, szRspSerial)
                if mjMgr.IsTuoGuan(nMember):
                    tick_mgr.RegisterOnceTick(100, mjMgr.RequestGang, [nMember, nOptMember, nCard])

                framework.LOGINFO("FFSCENE_PYTHON", "GasMj.Gang {0}, {1} ".format(json.dumps(listCard), nCard))
                bNextTurn = False
                continue

            # check gang with peng
            if check_hu_mgr.testGang(nCard, listCardEx, listJinPai) is True:
                rsp.ev_type = EMjEvent.ev_gang_with_peng
                rsp.ev_target = nOptMember
                rsp.ev_data = str(nCard)
                szRspSerial = rsp.SerializeToString()
                framework.send_msg_session(nMember, rpc_def.Gas2GacOnTouchGameEvent, szRspSerial)
                if mjMgr.IsTuoGuan(nMember):
                    tick_mgr.RegisterOnceTick(100, mjMgr.RequestGang, [nMember, nOptMember, nCard])

                framework.LOGINFO("FFSCENE_PYTHON", "GasMj.Gang {0}, {1} ".format(json.dumps(listCard), nCard))
                bNextTurn = False
                continue

            # check peng
            if check_hu_mgr.testPeng(nCard, listCard, listJinPai) is True:
                rsp.ev_type = EMjEvent.ev_peng
                rsp.ev_target = nOptMember
                rsp.ev_data = str(nCard)
                szRspSerial = rsp.SerializeToString()
                framework.send_msg_session(nMember, rpc_def.Gas2GacOnTouchGameEvent, szRspSerial)

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
        rsp = common_info_pb2.on_touch_event()
        rsp.ev_type = EMjEvent.ev_mo_pai
        rsp.ev_target = nOptMember
        rsp.ev_data = str(nCard)
        szRspSerial = rsp.SerializeToString()
        framework.send_msg_session(nOptMember, rpc_def.Gas2GacOnTouchGameEvent, szRspSerial)

        nCardType = check_hu_mgr.GetCardType(nCard)
        if nCardType == ECardType.eHuaPai:
            return

        # 摸到这张牌是不是能胡牌
        listCard = mjMgr.GetPosCardList(nPos)
        assert ((len(listCard) - 2) % 3 == 0)

        listJinPai = mjMgr.GetJinPaiList()

        bCanHu = check_hu_mgr.testHu(0, listCard, listJinPai)
        if bCanHu is True:
            rsp = common_info_pb2.on_touch_event()
            rsp.ev_type = EMjEvent.ev_hu_normal
            rsp.ev_target = nOptMember
            rsp.ev_data = str(nCard)
            szRspSerial = rsp.SerializeToString()
            framework.send_msg_session(nOptMember, rpc_def.Gas2GacOnTouchGameEvent, szRspSerial)
            framework.LOGINFO("FFSCENE_PYTHON", "GasMj.CanHu {0}, {0} ".format(json.dumps(listJinPai), json.dumps(mjMgr.DumpPos(nPos))))
            if mjMgr.IsTuoGuan(nOptMember) is True:
                tick_mgr.RegisterOnceTick(100, mjMgr.RequestHu, [nOptMember])

        if listCard.count(nCard) == 4:
            rsp.ev_type = EMjEvent.ev_gang_all
            rsp.ev_target = nOptMember
            rsp.ev_data = str(nCard)
            szRspSerial = rsp.SerializeToString()
            framework.send_msg_session(nOptMember, rpc_def.Gas2GacOnTouchGameEvent, szRspSerial)
            if mjMgr.IsTuoGuan(nOptMember):
                tick_mgr.RegisterOnceTick(100, mjMgr.RequestGang, [nOptMember, nOptMember, nCard])

            framework.LOGINFO("FFSCENE_PYTHON", "GasMj.GangAll {0}, {1} ".format(json.dumps(listCard), nCard))

        return True

    def EventBuHua(self, mjMgr, listData):
        nPos, nHuaPai, nCard = listData

        roomObj = mjMgr.GetRoomObj()
        listMember = roomObj.GetMemberList()
        nOptMember = roomObj.GetMemberIDByPos(nPos)

        rsp = common_info_pb2.on_touch_event()
        rsp.ev_type = EMjEvent.ev_bu_hua
        rsp.ev_target = nOptMember
        rsp.ev_data = "{0},{1}".format(nHuaPai, nCard)
        szRspSerial = rsp.SerializeToString()
        for nMember in listMember:
            framework.send_msg_session(nMember, rpc_def.Gas2GacOnTouchGameEvent, szRspSerial)

        return True

_mjEventMgr = GasMjEventMgr()
TouchEvent = _mjEventMgr.TouchEvent
