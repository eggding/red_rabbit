# -*- coding: utf-8 -*-
# @Author  : jh.feng

import ffext
import json
import random
import rpc.rpc_def as rpc_def
from util.enum_def import EGameRule, ECardType, EMjEvent, EStatusInRoom
import entity.rule_base as rule_base
import util.tick_mgr as tick_mgr
import check_hu as check_hu
import gas_mj_event_mgr as gas_mj_event_mgr
import cfg_py.parameter_common as parameter_common

import proto.common_info_pb2 as common_info_pb2

class GasMjRule(rule_base.GameRuleBase):
    def __init__(self, roomObj):
        super(GasMjRule, self).__init__(EGameRule.eGameRuleMj)

        self.m_roomObj = roomObj
        self.m_dictCfg = {}

        self.m_nMemberNum = None

        self.m_nMaxCardNum = check_hu.GetCardNum()

        # 局数
        self.m_nCurJu = 0
        self.m_nCurTurn = 0

        # 庄家
        self.m_nZhuang = 0

        # 轮到当前为那个玩家
        self.m_nCurOptMemberPos = 1

        # 当前摸到第几个牌
        self.m_nNextCardIndex = 0

        # 牌序
        self.m_listGlobalCard = []

        # jin pai
        self.m_listJinPai = []

        # 每个玩家的牌
        self.m_dictPosCarList = {}

        self.m_nEventTick = None
        self.m_nEventOptPlayer = None

        # peng/gang
        self.m_dictPosCarListEx = {}
        self.m_dictOptTick = {}
        self.m_dictPosHistory = {}
        self.m_dictPosEventRecord = {}

        # 各种计数
        self.m_dictTotalCount = {}
        self.m_dictEachJuScore = {}

        # 每个位置的事件触发缓存
        self.m_dictEventNoticePool = {}

        self.ResetScore()

    def ResetEventNoticePool(self):
        listMember = self.m_roomObj.GetMemberList()
        for nMember in listMember:
            nPos = self.m_roomObj.GetMemberPos(nMember)
            self.m_dictEventNoticePool[nPos] = []

    def GetScore(self, nPos):
        return self.m_dictEachJuScore.get(nPos, 0)

    def SetCurEventOptMember(self, nPlayerGID):
        self.m_nEventOptPlayer = nPlayerGID

    def GetCurEventOptMember(self):
        return self.m_nEventOptPlayer

    def GetCardListEx(self, nPos):
        return self.m_dictPosCarListEx[nPos]

    def GetCardListHist(self, nPos):
        return self.m_dictPosHistory[nPos]

    def GetRoomObj(self):
        return self.m_roomObj

    def IsTuoGuan(self, nMember):
        nVal = random.randint(1, 2)
        return nVal == 1
        # import entity.entity_mgr as entity_mgr
        # Player = entity_mgr.GetEntity(nMember)
        # assert Player is not None
        # return Player.IsInResidualState()

    def InitDefault(self):
        self.m_dictOptTick = {}
        self.m_nMemberNum = self.m_roomObj.GetMemberNum()
        self.m_nZhuang = 0

        self.m_nCurOptMemberPos = 1
        self.m_nCurTurn = 1
        self.m_nNextCardIndex = 0
        self.m_listGlobalCard = []
        self.m_listJinPai = []
        self.m_dictPosHistory = {}
        self.m_dictPosEventRecord = {}

        listRoomMember = self.m_roomObj.GetMemberList()
        nNum = len(listRoomMember)
        for nPos in xrange(1, nNum + 1):
            self.m_dictPosCarList[nPos] = []
            self.m_dictPosHistory[nPos] = []
            self.m_dictPosEventRecord[nPos] = []
            self.m_dictPosCarListEx[nPos] =  []

    def ResetScore(self):
        listRoomMember = self.m_roomObj.GetMemberList()
        nNum = len(listRoomMember)
        for nPos in xrange(1, nNum + 1):
            self.m_dictEachJuScore[nPos] = 0

    def GetZhuang(self):
        return self.m_nZhuang

    def GetCurTurn(self):
        return self.m_nCurTurn

    def GetCurJu(self):
        return self.m_nCurJu

    def GetCurOptMemberPos(self):
        return self.m_nCurOptMemberPos

    def GetCardRemain(self):
        return len(self.m_listGlobalCard) - self.m_nNextCardIndex

    def GetJinPaiList(self):
        return self.m_listJinPai

    def GetPosCardList(self, nPos):
        return self.m_dictPosCarList[nPos]

    def GetPosCardListAll(self, nPos):
        if nPos not in self.m_dictPosCarList:
            return []

        listCard = self.m_dictPosCarListEx[nPos][:]
        listCard.extend(self.m_dictPosCarList[nPos][:])
        return listCard

    def GetMaxJuNum(self):
        nChangNum = self.GetConfig()["total_start_game_num"]
        return nChangNum

    def InitWithCfg(self, dictCfg):
        self.m_dictCfg = dictCfg

    def GetQiPaiExpireSecond(self):
        return parameter_common.parameter_common[1]["参数"]

    def DingZhuang(self):
        """
        定庄
        :return:
        """
        listRoomMember = self.m_roomObj.GetMemberList()
        nRoomMemberNum = len(listRoomMember)
        assert nRoomMemberNum in (2, 4)

        if self.GetConfig().get("zhuang_pos") is not None:
            nRanPos = self.GetConfig().get("zhuang_pos")
        else:
            nRanPos = random.randint(0, nRoomMemberNum - 1)

        nZhuang = listRoomMember[nRanPos]
        self.m_nZhuang = nZhuang
        ffext.LOGINFO("FFSCENE_PYTHON", "GasMj.DingZhuang {0}, pos {1}".format(nZhuang, self.m_roomObj.GetMemberPos(nZhuang)))

    def XiPai(self):
        self.m_listGlobalCard = check_hu.GenCardArr()

        nLen = self.m_nMaxCardNum - 1
        while nLen > 0:
            if random.randint(1, 10) <= 8:
                nLen -= 1
                continue

            nPos = random.randint(0, nLen)
            nTmpVal = self.m_listGlobalCard[nLen]
            self.m_listGlobalCard[nLen] = self.m_listGlobalCard[nPos]
            self.m_listGlobalCard[nPos] = nTmpVal
            nLen -= 1

        ffext.LOGINFO("FFSCENE_PYTHON", "GasMj.XiPai {0}".format(json.dumps(self.m_listGlobalCard)))

    def GetNextPos(self):
        if self.m_nCurOptMemberPos == self.m_roomObj.GetMemberNum():
            self.m_nCurOptMemberPos = 1
        else:
            self.m_nCurOptMemberPos += 1

        return self.m_nCurOptMemberPos

    def GetCurPos(self):
        return self.m_nCurOptMemberPos

    def GetPrevPos(self, nPos):
        if nPos == 1:
            return self.m_roomObj.GetMemberNum()
        return nPos - 1

    def CheckBuHua(self, nPos, nCard=None):
        if nCard is not None:
            listTmp = [nCard]
        else:
            listTmp = self.m_dictPosCarList[nPos][:]

        bNewCardIsHuaPai = False
        nDstCard = None
        for nCard in listTmp:
            nCardType = check_hu.GetCardType(nCard)
            if nCardType != ECardType.eHuaPai:
                continue

            nNextCard = self.GetNextCard()
            self.m_dictPosCarList[nPos].remove(nCard)
            self.m_dictPosCarListEx[nPos].append(nCard)
            self.m_dictPosCarList[nPos].append(nNextCard)
            gas_mj_event_mgr.TouchEvent(self, EMjEvent.ev_bu_hua, [nPos, nCard, nNextCard])
            ffext.LOGINFO("FFSCENE_PYTHON", "GasMj.BuHua {0}, {1}, {2}".format(nPos, check_hu.GetCardNameChinese(nCard), check_hu.GetCardNameChinese(nNextCard)))

            if check_hu.GetCardType(nNextCard) == ECardType.eHuaPai:
                bNewCardIsHuaPai = True
                nDstCard = nNextCard

        if bNewCardIsHuaPai is False:
            # 八仙过海
            if check_hu.CheckBaXianGuoHai(self.m_dictPosCarListEx[nPos]) is True:
                gas_mj_event_mgr.TouchEvent(EMjEvent.ev_hu_ba_xian_guo_hai, [nPos])

        return bNewCardIsHuaPai, nDstCard

    def SerialEventList2Client(self):
        pass

    def AddEvent2NoticePoll(self):
        pass

    def MoPai(self, nPos, bCheckEventAndBuHua):
        assert self.m_nNextCardIndex < self.m_nMaxCardNum
        if self.m_nNextCardIndex >= self.m_nMaxCardNum - 12:
            self.OneJuEnd()
            return

        nCard = self.GetNextCard()
        self.m_dictPosCarList[nPos].append(nCard)
        self.StartQiPaiTick(nPos)
        self.SynOtherTouchEvent(EMjEvent.ev_mo_pai, self.m_roomObj.GetMemberIDByPos(nPos), 0, str(nCard))
        self.SynOrder()

        ffext.LOGINFO("FFSCENE_PYTHON",
                      "GasMj.MoPai {0}, {1}, {2} {3}".format(nPos, self.m_roomObj.GetMemberIDByPos(nPos),
                                                             check_hu.GetCardNameChinese(nCard),
                                                             len(self.m_dictPosCarList[nPos])))

        if bCheckEventAndBuHua is True:
            gas_mj_event_mgr.TouchEvent(self, EMjEvent.ev_mo_pai, [nPos, nCard])
            while True:
                bHaveHuaPai, nCard = self.CheckBuHua(nPos, nCard)
                self.SynOrder()
                if bHaveHuaPai is False:
                    break

    def DumpPos(self, nPos):
        szSerial = ""
        listCard = self.m_dictPosCarList[nPos][:]
        listTmp = check_hu.seprateArr(listCard, self.m_listJinPai)
        for listData in listTmp:
            szSerialTmp = ""
            for nCard in listData:
                szSerialTmp += check_hu.GetCardNameChinese(nCard) + ", "
            szSerial += szSerialTmp
        return szSerial

    def GetCardListByPos(self, nPos):
        return self.m_dictPosCarList[nPos]

    def GetConfig(self):
        return self.m_roomObj.GetConfig()

    def IsHalf(self):
        return self.GetConfig()["opt"] == 1

    def GetJinPaiNum(self):
        return 1 if self.IsHalf() else 2

    def KaiJin(self):
        nNum = self.GetJinPaiNum()
        self.m_listJinPai = []
        for _ in xrange(0, nNum):
            nCard = None
            while True:
                nCard = self.GetNextCard()
                if check_hu.GetCardType(nCard) != ECardType.eHuaPai and nCard not in self.m_listJinPai:
                    break

            assert nCard is not None
            self.m_listJinPai.append(nCard)

        gas_mj_event_mgr.TouchEvent(self, EMjEvent.ev_kai_jin, self.m_listJinPai[:])

        ffext.LOGINFO("FFSCENE_PYTHON", "GasMj.KaiJin {0}".format(json.dumps(self.m_listJinPai)))

    def GetNextCard(self):
        nCard = self.m_listGlobalCard[self.m_nNextCardIndex]
        self.m_nNextCardIndex += 1
        return nCard

    def FaPai(self):
        nPosZhuang = self.m_roomObj.GetMemberPos(self.m_nZhuang)
        self.m_nCurOptMemberPos = nPosZhuang
        listOrder = [nPosZhuang]
        for i in xrange(1, self.m_nMemberNum):
            nPos = self.GetNextPos()
            listOrder.append(nPos)

        self.m_nNextCardIndex = 0
        for nPos in listOrder:
            for i in xrange(0, 13):
                nCard = self.GetNextCard()
                self.m_dictPosCarList[nPos].append(nCard)

        self.m_nCurOptMemberPos = self.GetPrevPos(nPosZhuang)

    def NextTurn(self, bCheckEventAndBuHua=True):
        nPos = self.GetNextPos()
        self.m_nCurTurn += 1
        self.MoPai(nPos, bCheckEventAndBuHua)

    def GetEventExpireTime(self):
        return parameter_common.parameter_common[2]["参数"]

    def AutoQiPai(self, nPos):
        self.StopQiPaiTick(nPos)
        tingArr = check_hu.getTingNumArr(self.m_dictPosCarList[nPos], self.m_listJinPai)
        if len(tingArr) != 0:
            nIdx = random.randint(0, len(tingArr) - 1)
            nCardID = tingArr[nIdx]
        else:
            nCardIndex = random.randint(0, len(self.m_dictPosCarList[nPos]) - 1)
            nCardID = self.m_dictPosCarList[nPos][nCardIndex]

        self.m_dictPosCarList[nPos].remove(nCardID)
        self.m_dictPosHistory[nPos].append((self.m_nNextCardIndex - 1, nCardID))
        ffext.LOGINFO("FFSCENE_PYTHON", "GasMj.AutoQiPai {0}, {1}, {2}. {3} {4}".format(nPos, self.m_roomObj.GetMemberIDByPos(nPos), check_hu.GetCardNameChinese(nCardID), json.dumps(tingArr), len(self.m_dictPosCarList[nPos])))
        bCanNextTurn = gas_mj_event_mgr.TouchEvent(self, EMjEvent.ev_be_qi_pai, [nPos, nCardID])
        if bCanNextTurn is True:
            self.NextTurn()
        else:
            self.StartEventTick()

    def StopEventTick(self):
        if self.m_nEventTick is None:
            return
        tick_mgr.UnRegisterOnceTick(self.m_nEventTick)
        self.m_nEventTick = None

    def StartEventTick(self):
        self.StopEventTick()
        self.m_nEventTick = tick_mgr.RegisterOnceTick(self.GetEventExpireTime() * 1000, self.NextTurn)

    def OptQiPai(self, nPos, nCardID):
        listCard = self.m_dictPosCarList[nPos]
        assert nCardID in listCard

        self.StopQiPaiTick(nPos)
        listCard.remove(nCardID)
        self.m_dictPosHistory[nPos].append((self.m_nNextCardIndex - 1, nCardID))

        ffext.LOGINFO("FFSCENE_PYTHON", "GasMj.OptQiPai {0}, {1}".format(nPos, check_hu.GetCardNameChinese(nCardID)))
        bCanNextTurn = gas_mj_event_mgr.TouchEvent(self, EMjEvent.ev_be_qi_pai, [nPos, nCardID])
        if bCanNextTurn is True:
            self.NextTurn()
        else:
            self.StartEventTick()

    def StopQiPaiTick(self, nPos):
        nTick = self.m_dictOptTick.get(nPos)
        if nTick is not None:
            tick_mgr.UnRegisterOnceTick(nTick)
            self.m_dictOptTick[nPos] = None

    def StartQiPaiTick(self, nPos):
        self.StopQiPaiTick(nPos)

        nMember = self.m_roomObj.GetMemberIDByPos(nPos)
        import util.util as util
        if util.IsRobot(nMember) is True:
            nTick = tick_mgr.RegisterOnceTick(int(1 * 1000), self.AutoQiPai, nPos)
        else:
            nTick = tick_mgr.RegisterOnceTick(int(1 * 1000), self.AutoQiPai, nPos)

        self.m_dictOptTick[nPos] = nTick

    def CancelAutoTick(self):
        for nPos, nTickID in self.m_dictOptTick.iteritems():
            self.StopQiPaiTick(nPos)

    def RemoveCardFromList(self, listCard, nCardID, nRemoveNum):
        nNum = 0
        for i in xrange(0, nRemoveNum):
            for nOneCard in listCard:
                if check_hu.GetCardType(nCardID) != check_hu.GetCardType(nOneCard):
                    continue
                if check_hu.GetCardValue(nCardID) != check_hu.GetCardValue(nOneCard):
                    continue
                listCard.remove(nOneCard)
                nNum += 1
                break
        assert nNum == nRemoveNum

    def GacOpt(self, nPlayerGID, reqObj):
        nPos = self.m_roomObj.GetMemberPos(nPlayerGID)
        nOptType = reqObj.opt_type
        if nOptType == EMjEvent.ev_peng:
            if self.GetCurEventOptMember() != nPlayerGID:
                return
            nTargetMember, nCardID = map(int, reqObj.opt_data_str.split(","))
            self.RequestPeng([nPlayerGID, nTargetMember, nCardID])

        elif nOptType in (EMjEvent.ev_gang_all, EMjEvent.ev_gang_other, EMjEvent.ev_gang_with_peng):
            if self.GetCurEventOptMember() != nPlayerGID:
                return
            nTargetMember, nCardID = map(int, reqObj.opt_data_str.split(","))
            self.RequestGang([nPlayerGID, nTargetMember, nCardID])

        elif nOptType == EMjEvent.ev_pass:
            if self.GetCurEventOptMember() != nPlayerGID:
                return
            self.StopEventTick()
            self.NextTurn()

        elif nOptType == EMjEvent.ev_hu_normal:
            if self.GetCurOptMemberPos() != nPos:
                return
            self.RequestHu(nPlayerGID)

        elif nOptType == EMjEvent.ev_be_qi_pai:
            if self.GetCurOptMemberPos() != nPos:
                return
            nCardID = int(reqObj.opt_data_str)
            self.OptQiPai(nPos, nCardID)

        else:
            return

        import proto.opt_pb2 as opt_pb2
        rsp = opt_pb2.opt_rsp()
        rsp.ret = 0
        if nOptType not in (EMjEvent.ev_pass, EMjEvent.ev_hu_normal):
            listCard = self.m_dictPosCarList[nPos]
            for nCard in listCard:
                rsp.owner_card_list.append(nCard)

        if nOptType in (EMjEvent.ev_be_qi_pai, ):
            listListenCard = check_hu.getTingArr(self.m_dictPosCarList[nPos], self.GetJinPaiList())
            for nCard in listListenCard:
                rsp.listen_card.append(nCard)

        ffext.send_msg_session(nPlayerGID, rpc_def.Gas2GacRspOpt, rsp.SerializeToString())

    def ChangeOrder(self, nFromPos, nToPos):
        self.m_nCurOptMemberPos = nToPos
        self.StopQiPaiTick(nFromPos)
        self.StartQiPaiTick(nToPos)
        self.SynOrder()

    def RequestHu(self, nPlayerGID):
        nPlayerGID = nPlayerGID[0]
        nPos = self.m_roomObj.GetMemberPos(nPlayerGID)
        listCard = self.m_dictPosCarList[nPos]
        if check_hu.testHu(0, listCard, self.m_listJinPai) is False:
            return

        self.SynOtherTouchEvent(EMjEvent.ev_be_hu_normal, 0, nPlayerGID, "")
        ffext.LOGINFO("FFSCENE_PYTHON", "GasMj.Hu@@@@@ {0}, {1}, {2}".format(nPlayerGID, self.DumpPos(nPos), self.m_listJinPai))
        self.OneJuEnd(nPos)

    def RecordTouchEvent(self, nPos, listData):
        self.m_dictPosEventRecord[nPos].append(listData)

    def RequestGangAll(self, nPlayerGID, nTargetMember, nCardID):
        nPosOwner = self.m_roomObj.GetMemberPos(nPlayerGID)
        listCardOwner = self.m_dictPosCarList[nPosOwner]
        if listCardOwner.count(nCardID) != 4:
            return

        self.RemoveCardFromList(listCardOwner, nCardID, 4)
        for _ in xrange(0, 4):
            self.m_dictPosCarListEx[nPosOwner].append(nCardID)

        nCard = self.GetNextCard()
        self.m_dictPosCarList[nPosOwner].append(nCard)
        while True:
            bHaveHuaPai, nCard = self.CheckBuHua(nPosOwner, nCard)
            if bHaveHuaPai is False:
                break

        self.RecordTouchEvent(nPosOwner, [EMjEvent.ev_gang_all, nTargetMember, nCardID])
        self.ChangeOrder(nPosOwner, nPosOwner)
        self.StopEventTick()
        self.SynOtherTouchEvent(EMjEvent.ev_gang_all, 0, nPlayerGID, str(nCardID))

        self.SynCardInfoByType2All(self.m_roomObj.GetMemberPos(nPlayerGID),
                                   common_info_pb2.card_list_type.Value("eTypeShow"))

        ffext.LOGINFO("FFSCENE_PYTHON", "GasMj.RequestGangAll {0}".format(json.dumps([nPlayerGID, nTargetMember, nCardID, nPosOwner])))
        ffext.LOGINFO("FFSCENE_PYTHON", "GasMj.RequestGangRetAll {0}".format(self.DumpPos(nPosOwner)))


    def RequestGang(self, listData):
        nPlayerGID, nTargetMember, nCardID = listData
        if nPlayerGID == nTargetMember:
            self.RequestGangAll(nPlayerGID, nTargetMember, nCardID)
            return

        nPosTarget = self.m_roomObj.GetMemberPos(nTargetMember)
        tupleTmp = self.GetLastHistCardData(nPosTarget)
        nTurnIndex, nHistCardID = tupleTmp
        if nTurnIndex != self.m_nNextCardIndex - 1:
            return

        if nCardID != nHistCardID:
            return

        nPosOwner = self.m_roomObj.GetMemberPos(nPlayerGID)
        listCardOwner = self.m_dictPosCarList[nPosOwner]
        if check_hu.testGang(nCardID, listCardOwner, self.m_listJinPai) is True:
            bGangTypeWithPeng = False
        elif check_hu.testGang(nCardID, self.m_dictPosCarListEx[nPosOwner], self.m_listJinPai) is True:
                bGangTypeWithPeng = True
        else:
            return

        if bGangTypeWithPeng is False:
            self.RemoveCardFromList(listCardOwner, nCardID, 3)
            for _ in xrange(0, 4):
                self.m_dictPosCarListEx[nPosOwner].append(nCardID)
        else:
            self.m_dictPosCarListEx[nPosOwner].append(nCardID)

        nCard = self.GetNextCard()
        self.m_dictPosCarList[nPosOwner].append(nCard)
        while True:
            bHaveHuaPai, nCard = self.CheckBuHua(nPosOwner, nCard)
            if bHaveHuaPai is False:
                break

        self.ChangeOrder(nPosTarget, nPosOwner)
        self.StopEventTick()
        self.SynOtherTouchEvent(EMjEvent.ev_gang_with_peng if bGangTypeWithPeng is True else EMjEvent.ev_gang_other,
                                nTargetMember, nPlayerGID, str(nCardID))

        if bGangTypeWithPeng is True:
            self.RecordTouchEvent(nPosOwner, [EMjEvent.ev_gang_with_peng, nTargetMember, nCardID])
            ffext.LOGINFO("FFSCENE_PYTHON", "GasMj.RequestGangPeng {0}".format(json.dumps([nPlayerGID, nTargetMember, nCardID, nPosOwner])))
            ffext.LOGINFO("FFSCENE_PYTHON", "GasMj.RequestGangRetPeng {0}".format(self.DumpPos(nPosOwner)))
        else:
            self.RecordTouchEvent(nPosOwner, [EMjEvent.ev_gang_other, nTargetMember, nCardID])
            ffext.LOGINFO("FFSCENE_PYTHON", "GasMj.RequestGangOther {0}".format(json.dumps([nPlayerGID, nTargetMember, nCardID, nPosOwner])))
            ffext.LOGINFO("FFSCENE_PYTHON", "GasMj.RequestGangRetOther {0}".format(self.DumpPos(nPosOwner)))

        self.SynCardInfoByType2All(nPosTarget, common_info_pb2.card_list_type.Value("eTypeHist"))
        self.SynCardInfoByType2All(self.m_roomObj.GetMemberPos(nPlayerGID),
                                   common_info_pb2.card_list_type.Value("eTypeShow"))


    def RequestPeng(self, listData):
        nPlayerGID, nTargetMember, nCardID = listData
        nPosTarget = self.m_roomObj.GetMemberPos(nTargetMember)
        tupleTmp = self.GetLastHistCardData(nPosTarget)
        nTurnIndex, nHistCardID = tupleTmp
        if nTurnIndex != self.m_nNextCardIndex - 1:
            return

        if nCardID != nHistCardID:
            return

        nPosOwner = self.m_roomObj.GetMemberPos(nPlayerGID)
        listCardOwner = self.m_dictPosCarList[nPosOwner]
        if check_hu.testPeng(nCardID, listCardOwner, self.m_listJinPai) is False:
            return

        self.RemoveCardFromList(listCardOwner, nCardID, 2)
        for _ in xrange(0, 3):
            self.m_dictPosCarListEx[nPosOwner].append(nCardID)

        self.StopEventTick()
        self.ChangeOrder(nPosTarget, nPosOwner)

        self.RecordTouchEvent(nPosOwner, [EMjEvent.ev_peng, nTargetMember, nCardID])
        self.SynOtherTouchEvent(EMjEvent.ev_be_peng, nTargetMember, nPlayerGID, str(nCardID))
        self.SynCardInfoByType2All(nPosTarget, common_info_pb2.card_list_type.Value("eTypeHist"))
        self.SynCardInfoByType2All(self.m_roomObj.GetMemberPos(nPlayerGID),
                                   common_info_pb2.card_list_type.Value("eTypeShow"))
        ffext.LOGINFO("FFSCENE_PYTHON", "GasMj.RequestPeng {0}".format(json.dumps([nPlayerGID, nTargetMember, nCardID, nPosOwner])))
        ffext.LOGINFO("FFSCENE_PYTHON", "GasMj.RequestPengRet {0}".format(self.DumpPos(nPosOwner)))

    def SynCardInfoByType2All(self, nPos, nType):
        rsp = common_info_pb2.syn_card_list_by_type()
        rsp.pos = nPos
        rsp.type = nType

        if nType == common_info_pb2.card_list_type.Value("eTypeHave"):
            rsp.card_list.append(self.SerialList2Str(self.m_dictPosCarList[nPos]))
        elif nType == common_info_pb2.card_list_type.Value("eTypeShow"):
            rsp.card_list.append(self.SerialTouchEventData(nPos))
        elif nType == common_info_pb2.card_list_type.Value("eTypeHist"):
            rsp.card_list.append(self.SerialList2Str(self.m_dictPosHistory[nPos]))
        else:
            assert False

        szRspSerial = rsp.SerializeToString()
        for nMember in self.m_roomObj.GetMemberList():
            ffext.send_msg_session(nMember, rpc_def.Gas2GacRetSynCardListByType, szRspSerial)

    def SynOtherTouchEvent(self, nEventType, nTarget, nTargetSrc, szOptData, listUnNoticePlayer=None):
        rsp = common_info_pb2.on_touch_event()
        rsp.ev_type = nEventType
        rsp.ev_target = nTarget
        rsp.ev_target_src = nTargetSrc
        rsp.ev_data = szOptData
        szRspSerial = rsp.SerializeToString()
        for nMember in self.m_roomObj.GetMemberList():
            if listUnNoticePlayer is not None and nMember in listUnNoticePlayer:
                continue
            ffext.send_msg_session(nMember, rpc_def.Gas2GacOnTouchGameEvent, szRspSerial)

    def GetAllCardList(self, nPos):
        listTmp = self.m_dictPosCarListEx[nPos][:]
        listTmp.extend(self.m_dictPosCarList[nPos])
        return listTmp

    def SerialList2Str(self, listData):
        szRet = ""
        for nData in listData:
            if len(szRet) != 0:
                szRet += ","
            szRet += str(nData)
        return szRet

    def GetHuType(self):
        return EMjEvent.ev_hu_normal

    def ShowResultOne(self, nWinnerPos):
        import proto.show_result_pb2 as show_result_pb2
        rsp = show_result_pb2.show_result_one_rsp()
        rsp.room_id = self.m_roomObj.GetRoomID()
        rsp.cur_round = self.m_nCurJu
        rsp.total_round = self.GetMaxJuNum()
        rsp.master_pos = self.m_roomObj.GetMemberPos(self.m_nZhuang)
        rsp.winner_pos = nWinnerPos
        rsp.golden_card_list = self.SerialList2Str(self.m_listJinPai)
        rsp.hu_type = self.GetHuType()

        import check_hu as check_hu_mgr
        import entity.entity_mgr as entity_mgr
        for nMember in self.m_roomObj.GetMemberList():
            dataInfo = rsp.list_data.add()

            nPos = self.m_roomObj.GetMemberPos(nMember)
            Player = entity_mgr.GetEntity(nMember)
            dataInfo.wecaht_info = Player.GetWeChatInfo().encode('utf-8')
            dataInfo.player_id = nMember
            dataInfo.pos = nPos

            tmpCardList = self.m_dictPosCarList[nPos]
            tmpCardList.extend(self.m_dictPosCarListEx[nPos])
            dataInfo.card_list = self.SerialList2Str(tmpCardList)

            listHuaPai = []
            for tupleInfo in self.m_dictPosHistory[nPos]:
                _, nCard = tupleInfo
                if check_hu_mgr.IsHuaPai(nCard) is False:
                    continue
                listHuaPai.append(nCard)
            dataInfo.hua_list = self.SerialList2Str(listHuaPai)

            self.GetMemberAllCardInfo(nPos, dataInfo.card_info, bSynHaveCard=True)
            dataInfo.event_list = self.GetEventStr()
            dataInfo.total_score = self.GetScore(nPos)

        for nMember in self.m_roomObj.GetMemberList():
            ffext.send_msg_session(nMember, rpc_def.Gas2GacRetShowResultOne, rsp.SerializeToString())

    def GetLastHistCard(self, nPos):
        listCardHist = self.m_dictPosHistory[nPos]
        nSize = len(listCardHist)
        assert nSize != 0
        nCardOrder, nCard = listCardHist[nSize - 1]
        return nCard

    def GetLastHistCardData(self, nPos):
        listCardHist = self.m_dictPosHistory[nPos]
        nSize = len(listCardHist)
        assert nSize != 0
        return listCardHist[nSize - 1]

    def SerialTouchEventData(self, nPos):
        szRet = ""
        listTouchEvent = self.m_dictPosEventRecord[nPos]
        if len(listTouchEvent) == 0:
            return szRet
        for tupleOneEvent in listTouchEvent:
            nEvent, nTarget, nCard = tupleOneEvent
            if nEvent in (EMjEvent.ev_gang_all, EMjEvent.ev_gang_other, EMjEvent.ev_gang_with_peng):
                szTmp = "{0}:{1}".format(nEvent, nCard)
            elif nEvent == EMjEvent.ev_peng:
                szTmp = "{0}:{1}".format(nEvent, nCard)
            else:
                szTmp = ""
            if len(szRet) != 0:
                szRet += "|"
            szRet += szTmp
        return szRet

    def GetMemberAllCardInfo(self, nPos, rsp, bSynHaveCard=False):
        """
        :param nPos: 
        :param rsp:
        :param bSynHaveCard: 
        :return: 
        """
        rsp.pos = nPos
        if nPos not in self.m_dictPosCarList:
            rsp.card_num = 0
            rsp.list_card_show = ""
            return

        listCardHave = self.m_dictPosCarList[nPos]
        if bSynHaveCard is True:
            for nCard in listCardHave:
                rsp.list_card_have.append(nCard)

        rsp.card_num = len(listCardHave)

        listCardHist = self.m_dictPosHistory[nPos]
        for tInfo in listCardHist:
            _, nCard = tInfo
            rsp.list_card_hist.append(nCard)

        rsp.list_card_show = self.SerialTouchEventData(nPos)

    def GetEventStr(self):
        return ""

    def IncAllMemberPlayNum(self):
        import entity.entity_mgr as entity_mgr
        for nMember in self.m_roomObj.GetMemberList():
            Player = entity_mgr.GetEntity(nMember)
            assert Player is not None
            Player.AddTotalPlayNum()

    def ShowResultAll(self, nWinnerPos):
        import proto.show_result_pb2 as show_result_pb2
        rsp = show_result_pb2.show_result_all_rsp()
        rsp.room_id = self.m_roomObj.GetRoomID()
        rsp.cur_round = self.m_nCurJu
        rsp.total_round = self.GetMaxJuNum()

        nRoomMaster = self.m_roomObj.GetMemberPos()
        rsp.room_master_pos = self.m_roomObj.GetMemberPos(nRoomMaster)
        rsp.winner_pos = nWinnerPos

        import entity.entity_mgr as entity_mgr
        for nMember in self.m_roomObj.GetMemberList():
            allData = rsp.list_data.add()

            Player = entity_mgr.GetEntity(nMember)
            assert Player is not None
            allData.player_id = nMember
            allData.pos = self.m_roomObj.GetMemberPos(nMember)
            allData.wecaht_info = Player.GetWeChatInfo().encode("utf-8")

            dictData = self.m_dictTotalCount[allData.pos]
            allData.hu_num = dictData.get("hu_num", 0)
            allData.dan_you_num = dictData.get("dan_you_num", 0)
            allData.shuang_you_num = dictData.get("shuang_you_num", 0)
            allData.sam_you_num = dictData.get("sam_you_num", 0)
            allData.kai_gang_num = dictData.get("kai_gang_num", 0)
            allData.total_score = dictData.get("total_score", 0)

        for nMember in self.m_roomObj.GetMemberList():
            ffext.send_msg_session(nMember, rpc_def.Gas2GacRetShowResultAll, rsp.SerializeToString())

    def InitHistCounterDefault(self):
        listMember = self.m_roomObj.GetMemberList()
        for nMember in listMember:
            nPos = self.m_roomObj.GetMemberPos(nMember)
            self.m_dictTotalCount[nPos] = {
                "total_score": 0,
                "hu_num": 0,
                "kai_gang_num": 0,
                "dan_you_num": 0,
                "shuang_you_num": 0,
                "sam_you_num": 0,
            }

    def CalAllMemberScore(self, nWinnerPos):
        listMember = self.m_roomObj.GetMemberList()
        for nMember in listMember:
            nPos = self.m_roomObj.GetMemberPos(nMember)
            nScore = 0
            if nWinnerPos == nPos:
                nScore += 1
            self.m_dictEachJuScore[nPos] += nScore

        # process total score
        for nPos, nScore in self.m_dictEachJuScore.iteritems():
            self.m_dictTotalCount[nPos]["total_score"] += nScore

    def AddCounterRecordHist(self, nWinnerPos):
        if nWinnerPos == 0:
            return
        self.m_dictTotalCount[nWinnerPos]["hu_num"] += 1
        for nPos, listRecordData in self.m_dictPosEventRecord.iteritems():
            if 0 == len(listRecordData):
                continue
            for tupleRecordData in listRecordData:
                nEvent, nTarget, nCard = tupleRecordData
                if nEvent in (EMjEvent.ev_gang_with_peng, EMjEvent.ev_gang_other, EMjEvent.ev_gang_all):
                    self.m_dictTotalCount[nPos]["kai_gang_num"] += 1

    def OneJuEnd(self, nWinnerPos=None):
        if nWinnerPos is None:
            nWinnerPos = 0

        self.CancelAutoTick()
        self.AddCounterRecordHist(nWinnerPos)
        self.CalAllMemberScore(nWinnerPos)
        self.IncAllMemberPlayNum()
        self.ShowResultOne(nWinnerPos)

        if self.m_nCurJu >= self.GetMaxJuNum():
            self.ShowResultAll(nWinnerPos)
            self.GameEnd()
        else:
            self.InitDefault()
            self.m_roomObj.ChangeRoomStateToWaiting()

    def SynOrder(self):
        import proto.opt_pb2 as opt_pb2
        rsp = opt_pb2.syn_game_order()
        rsp.room_id = self.m_roomObj.GetRoomID()
        rsp.cur_game_num = self.GetMaxJuNum()
        rsp.cur_round = self.m_nCurJu
        rsp.cur_turn = self.m_nCurTurn
        rsp.remain_card_num = len(self.m_listGlobalCard) - self.m_nNextCardIndex
        rsp.opt_pos = self.m_nCurOptMemberPos

        listMember = self.m_roomObj.GetMemberList()
        for nMember in listMember:
            ffext.send_msg_session(nMember, rpc_def.Gac2GasSynGameOrder, rsp.SerializeToString())

    def StartJu(self):
        """
        开启新的一局
        :return:
        """
        self.CancelAutoTick()
        self.InitDefault()

        ffext.LOGINFO("FFSCENE_PYTHON", "GasMj.StartJu {0}".format(self.m_nCurJu))
        self.m_nCurJu += 1

        szCardOrder = self.GetConfig().get("card_order")
        if szCardOrder is not None:
            self.m_listGlobalCard = map(int, szCardOrder.split(","))

            nPosZhuang = None
            for nPos in xrange(1, 5):
                listCard = map(int, self.GetConfig().get("pos_{0}_card".format(nPos)).split(","))
                self.m_dictPosCarList[nPos] = listCard
                if len(listCard) == 14:
                    nPosZhuang = nPos
            assert nPosZhuang is not None

            self.m_nZhuang = self.m_roomObj.GetMemberIDByPos(nPosZhuang)
            nZhuangExCard = self.m_dictPosCarList[nPosZhuang][-1:][0]
            self.m_dictPosCarList[nPosZhuang] = self.m_dictPosCarList[nPosZhuang][:-1]

            listTmp = [nZhuangExCard]
            listTmp.extend(self.m_listGlobalCard)
            self.m_listGlobalCard = listTmp

            self.m_nNextCardIndex = 0
            self.m_nCurOptMemberPos = self.GetPrevPos(nPosZhuang)

            ffext.LOGINFO("FFSCENE_PYTHON", "GasMj.XiPai {0}".format(json.dumps(self.m_listGlobalCard)))
            ffext.LOGINFO("FFSCENE_PYTHON", "GasMj.DingZhuang {0}, pos {1}".format(self.m_nZhuang, self.m_roomObj.GetMemberPos(self.m_nZhuang)))

        else:
            self.DingZhuang()
            self.XiPai()
            self.FaPai()

        self.KaiJin()
        listMember = self.m_roomObj.GetMemberList()
        for nMember in listMember:
            self.m_roomObj.SynGameInfo(nMember, bSynAll=False)

        self.NextTurn(bCheckEventAndBuHua=False)

        while True:
            bContinueBuHua = False
            for nPos in xrange(1, self.m_nMemberNum + 1):
                bHaveHuaPai, _ = self.CheckBuHua(nPos)
                if bHaveHuaPai is True:
                    bContinueBuHua = True
            if bContinueBuHua is False:
                break

        for i in xrange(1, self.m_nMemberNum + 1):
            ffext.LOGINFO("FFSCENE_PYTHON", "GasMj.FaPai {0}, {1}".format(i, self.DumpPos(i)))


    def GameStart(self):
        self.InitHistCounterDefault()
        self.ResetScore()
        self.StartJu()

    def GameEnd(self):
        self.m_roomObj.OnGameEnd()
        self.m_roomObj = None

    def OnMemberExit(self, nMemberGID):
        pass

    def OnMemberEnter(self, nMemberGID):
        pass