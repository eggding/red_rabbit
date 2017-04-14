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

g_bTick = False

def StartTestTick(a):
    print("dbs StartTestTick")
    ffext.once_timer(1000, StartTestTick, 1)

@ffext.reg_service(rpc_def.DbsTest)
def DbsTest(dictSerial):
    global g_bTick
    if g_bTick is False:
        g_bTick = True
        StartTestTick(1)
    # ffext.once_timer(1000, ShowDbsQueueStatus, 1)
    szAuthKey = dictSerial[dbs_def.PARAMS]
    db_mgr.Add2JobQueue(dictSerial[dbs_def.SRC_SCENE], dictSerial[dbs_def.CB_ID], szAuthKey, dbs_opt.ImpDbsTest, szAuthKey)

@ffext.reg_service(rpc_def.DbsCreateUserSession)
def DbsCreateUserSession(dictSerial):
    szAuthKey = dictSerial[dbs_def.PARAMS]
    db_mgr.Add2JobQueue(dictSerial[dbs_def.SRC_SCENE], dictSerial[dbs_def.CB_ID], None, dbs_opt.ImpDbsCreateUserSession, szAuthKey)

@ffext.reg_service(rpc_def.DbsLoadPlayerData)
def DbsLoadPlayerData(dictSerial):
    session = dictSerial[dbs_def.PARAMS]
    db_mgr.Add2JobQueue(dictSerial[dbs_def.SRC_SCENE], dictSerial[dbs_def.CB_ID], session, dbs_opt.ImpDbsLoadPlayerData)

@ffext.reg_service(rpc_def.DbsGetUserSession)
def DbsGetUserSession(dictSerial):
    szAuthKey = dictSerial[dbs_def.PARAMS]
    def _imp(conn, job):
        print("DbsGetUserSession._Imp")
        sql = "select `SESSION_ID` FROM `account` WHERE `ACCOUNT_ID` = '%s'" % (szAuthKey)
        conn.query(sql, db_mgr.OnOneDbQueryDone, job)
    db_mgr.Add2JobQueue(dictSerial[dbs_def.SRC_SCENE], dictSerial[dbs_def.CB_ID], None, _imp)
