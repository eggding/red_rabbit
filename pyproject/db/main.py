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

@ffext.reg_service(rpc_def.DbsCreateUserSession)
def DbsCreateUserSession(dictSerial):
    szAuthKey = dictSerial[dbs_def.PARAMS]
    db_mgr.Add2JobQueue(dictSerial[dbs_def.SRC_SCENE], dictSerial[dbs_def.CB_ID], 0, dbs_opt.ImpDbsCreateUserSession, szAuthKey)

@ffext.reg_service(rpc_def.DbsLoadPlayerData)
def DbsLoadPlayerData(dictSerial):
    session = dictSerial[dbs_def.PARAMS]
    db_mgr.Add2JobQueue(dictSerial[dbs_def.SRC_SCENE], dictSerial[dbs_def.CB_ID], session, dbs_opt.ImpDbsLoadPlayerData)

@ffext.reg_service(rpc_def.DbsGetUserSession)
def DbsGetUserSession(dictSerial):
    szAuthKey = dictSerial[dbs_def.PARAMS]
    def _imp(conn, job):
        sql = "select `SESSION_ID` FROM `account` WHERE `ACCOUNT_ID` = '%s'" % (szAuthKey)
        conn.query(sql, db_mgr.OnOneDbQueryDone, job)
    db_mgr.Add2JobQueue(dictSerial[dbs_def.SRC_SCENE], dictSerial[dbs_def.CB_ID], 0, _imp)