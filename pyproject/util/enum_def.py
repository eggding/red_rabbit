# -*- coding: utf-8 -*-
# @Author  : jh.feng

import entity.const_entity as const_entity

class EIdType(const_entity.Const):
    eIdTypePlayer = 1
    eIdTypeRoom = 2

class EMoneyType(const_entity.Const):
    eYuanbao = 1

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