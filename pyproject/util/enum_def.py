# -*- coding: utf-8 -*-
# @Author  : jh.feng

import entity.const_entity as const_entity

class EDbsOptType(const_entity.Const):
    eQuery = 1
    eUpdate = 2
    eDel = 3
    eInsert = 4

class ECardType(const_entity.Const):
    eWanZi = 1
    eTongZi = 2
    eSuoZi = 3
    eZiPai = 4
    eHuaPai = 5

import proto.common_info_pb2 as common_info_pb2

class EMjEvent(const_entity.Const):
    ev_gang_with_peng = 101
    ev_gang_other = 102
    ev_gang_all = 103
    ev_peng = 111
    ev_chi = 112
    ev_pass = 117
    ev_cha_pai = 118
    ev_dan_you = 121
    ev_shuang_you = 122
    ev_san_you = 123
    ev_hu_normal = 181
    ev_hu_cha_hua = 182
    ev_hu_qiang_gang = 183
    ev_hu_qiang_jin = 184
    ev_hu_san_jin_dao = 185
    ev_hu_si_jin_dao = 186
    ev_hu_wu_jin_dao = 187
    ev_hu_liu_jin_dao = 188
    ev_hu_ba_xian_guo_hai = 189
    ev_hu_shi_san_yao = 190
    ev_hu_qi_dui_zi = 191
    ev_bu_hua = 213
    ev_kai_jin = 214
    ev_mo_pai = 215
    ev_be_qi_pai = 216
    ev_be_dan_you = 221
    ev_be_shuang_you = 222
    ev_be_san_you = 223
    ev_be_fen_bing_1 = 224
    ev_be_fen_bing_2 = 225
    ev_be_peng = 226
    ev_be_gang = 227
    ev_be_gang_hu = 228
    ev_be_cha = 229
    ev_be_hu_normal = 281
    ev_be_hu_cha_hua = 282
    ev_be_hu_qiang_gang = 283
    ev_be_hu_qiang_jin = 284
    ev_be_hu_san_jin_dao = 285
    ev_be_hu_si_jin_dao = 286
    ev_be_hu_wu_jin_dao = 287
    ev_be_hu_liu_jin_dao = 288
    ev_be_hu_ba_xian_guo_hai = 289
    ev_be_hu_shi_san_yao = 290
    ev_be_hu_qi_dui_zi = 291

class EMoneyType(const_entity.Const):
    eZhuanShi = 1

class EMemberEvent(const_entity.Const):
    evMemberEnter = 1 # 玩家进入房间事件
    evMemberExit = 2 # 玩家推出房间事件

class EGameRule(const_entity.Const):
    eGameRuleMj = 1

class EPlayerState(const_entity.Const):
    eDisConnect = 0
    eOnline = 1

class EIdType(const_entity.Const):
    eIdTypePlayer = 1
    eIdTypeRoom = 2

class RoomMemberProperty(const_entity.Const):
    ePos = 0
    eStatus = 1

class EStatusInRoom(const_entity.Const):
    eUnReady = 1
    eReady = 2
    eOffline = 3
    ePlaying = 4
    eExitRoom = 5

    eWaiting = 101
    eRunning = 202

class EServiceNotInCluster(const_entity.Const):
    eServiceLog = "log"
    eServiceHttp = "http"

class ELogType(const_entity.Const):
    eLogin = "login"
    eLogOut = "logout"