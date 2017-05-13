# coding=UTF-8

import ffext, ff
import sys
sys.path.append("./pyproject")

import rpc.scene_def as scene_def
import db.dbs_mgr_mp as db_mgr
import rpc.rpc_def as rpc_def
import db.dbs_opt_mp as dbs_opt


@ffext.reg_service(rpc_def.DbsUpdateID)
def DbsUpdateID(dictSerial):
    db_mgr.GenJob(dictSerial, "ImpUpdateID")

@ffext.reg_service(rpc_def.DbsGetIDData)
def DbsGetIDData(dictSerial):
    db_mgr.GenJob(dictSerial, "ImpGetIDData")

@ffext.reg_service(rpc_def.DbsGetRoomIDSector)
def DbsGetRoomIDSector(dictSerial):
    pass

@ffext.reg_service(rpc_def.DbsPersistentPlayerData)
def DbsPersistentPlayerData(dictSerial):
    db_mgr.GenJob(dictSerial, "ImpDbsPersistentPlayerData")

@ffext.reg_service(rpc_def.DbsTest)
def DbsTest(dictSerial):
    db_mgr.GenJob(dictSerial, "ImpDbsTest")

@ffext.reg_service(rpc_def.DbsCreateUserSession)
def DbsCreateUserSession(dictSerial):
    db_mgr.GenJob(dictSerial, "ImpDbsCreateUserSession")

@ffext.reg_service(rpc_def.DbsLoadPlayerData)
def DbsLoadPlayerData(dictSerial):
    db_mgr.GenJob(dictSerial, "ImpDbsLoadPlayerData")

@ffext.reg_service(rpc_def.DbsGetUserSession)
def DbsGetUserSession(dictSerial):
    db_mgr.GenJob(dictSerial, "ImpGetUserSession")

@ffext.reg_service(rpc_def.Peer)
def Peer(dictSerial):
    ffext.call_service(scene_def.GATE_MASTER, rpc_def.RspPeer, {"service": ff.service_name})

@ffext.reg_service(rpc_def.OnAllServiceStartUp)
def OnAllServiceStartUp(dictSerial):
    pass

def A():
    ffext.call_service(scene_def.GATE_MASTER, rpc_def.OnServiceConn, {"service": ff.service_name})

import util.tick_mgr as tick_mgr
tick_mgr.RegisterOnceTick(100, A)
