# coding=UTF-8
import os
import time
import ffext
import sys
sys.path.append("./pyproject")

import db.dbs_mgr as db_mgr
import rpc.rpc_def as rpc_def
import dbs_def as dbs_def
import db.dbs_opt as dbs_opt

@ffext.reg_service(rpc_def.DbsTest)
def DbsTest(dictSerial):
    szAuthKey = dictSerial[dbs_def.PARAMS]
    nChannel = dictSerial[dbs_def.USE_CHANNEL]
    db_mgr.Add2JobQueue(dictSerial[dbs_def.SRC_SCENE], dictSerial[dbs_def.CB_ID], szAuthKey, dbs_opt.ImpDbsTest, szAuthKey, nChannel=nChannel)

@ffext.reg_service(rpc_def.DbsCreateUserSession)
def DbsCreateUserSession(dictSerial):
    szAuthKey = dictSerial[dbs_def.PARAMS]
    nChannel = dictSerial[dbs_def.USE_CHANNEL]
    db_mgr.Add2JobQueue(dictSerial[dbs_def.SRC_SCENE], dictSerial[dbs_def.CB_ID], None, dbs_opt.ImpDbsCreateUserSession, szAuthKey, nChannel=nChannel)

@ffext.reg_service(rpc_def.DbsLoadPlayerData)
def DbsLoadPlayerData(dictSerial):
    session = dictSerial[dbs_def.PARAMS]
    nChannel = dictSerial[dbs_def.USE_CHANNEL]
    db_mgr.Add2JobQueue(dictSerial[dbs_def.SRC_SCENE], dictSerial[dbs_def.CB_ID], session, dbs_opt.ImpDbsLoadPlayerData, nChannel=nChannel)

@ffext.reg_service(rpc_def.DbsGetUserSession)
def DbsGetUserSession(dictSerial):
    szAuthKey = dictSerial[dbs_def.PARAMS]
    nChannel = dictSerial[dbs_def.USE_CHANNEL]
    def _imp(conn, job):
        print("DbsGetUserSession._Imp")
        sql = "select `SESSION_ID` FROM `account` WHERE `ACCOUNT_ID` = '%s'" % (szAuthKey)
        conn.query(sql, db_mgr.OnOneDbQueryDone, job)
    db_mgr.Add2JobQueue(dictSerial[dbs_def.SRC_SCENE], dictSerial[dbs_def.CB_ID], None, _imp, nChannel=nChannel)
