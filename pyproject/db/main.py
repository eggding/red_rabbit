# coding=UTF-8

import ffext
import sys
sys.path.append("./pyproject")

import db.dbs_mgr as db_mgr
import rpc.rpc_def as rpc_def
import db.dbs_opt as dbs_opt

@ffext.reg_service(rpc_def.DbsGetRoomIDSector)
def DbsGetRoomIDSector(dictSerial):
    db_mgr.GenJob(dictSerial, dbs_opt.ImpDbsGetRoomIDSector)

@ffext.reg_service(rpc_def.DbsPersistentPlayerData)
def DbsPersistentPlayerData(dictSerial):
    db_mgr.GenJob(dictSerial, dbs_opt.ImpDbsPersistentPlayerData)

@ffext.reg_service(rpc_def.DbsTest)
def DbsTest(dictSerial):
    db_mgr.GenJob(dictSerial, dbs_opt.ImpDbsTest)

@ffext.reg_service(rpc_def.DbsCreateUserSession)
def DbsCreateUserSession(dictSerial):
    db_mgr.GenJob(dictSerial, dbs_opt.ImpDbsCreateUserSession)

@ffext.reg_service(rpc_def.DbsLoadPlayerData)
def DbsLoadPlayerData(dictSerial):
    db_mgr.GenJob(dictSerial, dbs_opt.ImpDbsLoadPlayerData)

@ffext.reg_service(rpc_def.DbsGetUserSession)
def DbsGetUserSession(dictSerial):
    db_mgr.GenJob(dictSerial, dbs_opt.ImpGetUserSession)
