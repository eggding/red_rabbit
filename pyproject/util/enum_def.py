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

class EMjEvent(const_entity.Const):
    ev_gang_with_peng = 1 # 杠其他人，自己的3个牌有1个是碰回来的
    ev_gang_other = 2 # 杠其他人，自己摸了3个
    ev_gang_all = 3 # 自己摸回来4个一样的杠牌

    ev_peng = 11 # 碰
    ev_chi = 12 # 吃
    ev_bu_hua = 13 # 补花
    ev_kai_jin = 14 # 开金
    ev_mo_pai = 15 # 摸牌
    ev_qi_pai = 16 # 弃牌
    ev_pass = 17
    ev_cha_pai = 18

    ev_dan_you = 21 # 单游
    ev_shuang_you = 22 # 双游
    ev_san_you = 23 # 三游

    ev_fen_bing_1 = 24 # 1
    ev_fen_bing_2 = 25 # 2

    ev_hu_normal = 81 # 普通胡
    ev_hu_cha_hua = 82 # 查花胡
    ev_hu_qiang_gang = 83 # 抢杠胡
    ev_hu_qiang_jin = 84 # 枪金胡
    ev_hu_san_jin_dao = 85 # 三金倒
    ev_hu_si_jin_dao = 86 # 四金倒
    ev_hu_wu_jin_dao = 87 # 五金倒
    ev_hu_liu_jin_dao = 88
    ev_hu_ba_xian_guo_hai = 89 # 八仙过海
    ev_hu_shi_san_yao = 90 # 十三幺
    ev_hu_qi_dui_zi = 91 # 七对子

    ev_syn_card = 149 # 同步自己的牌序
    ev_syn_order = 150 # 同步当前局数、第几轮、出牌顺序顺序

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
    eUnReady = 0
    eReady = 1
    eOffline = 2
    ePlaying = 3

    eWaiting = 101
    eRunning = 102