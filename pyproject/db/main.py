# coding=UTF-8

import ffext
import sys
sys.path.append("./pyproject")

import util.tick_mgr as tick_mgr
import db.dbs_mgr_mp as db_mgr
import rpc.rpc_def as rpc_def
import db.dbs_opt_mp as dbs_opt

@ffext.reg_service(rpc_def.DbsGetRoomIDSector)
def DbsGetRoomIDSector(dictSerial):
    db_mgr.GenJob(dictSerial, "ImpDbsGetRoomIDSector")

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
