# -*- coding: utf-8 -*-
# @Author  : jh.feng

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

class GccRoomMgr(object):
    def __init__(self):
        self.m_dictPlayer2RoomID = {}
        self.m_dictRoomID2GasID = {}