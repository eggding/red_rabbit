# coding=UTF-8
import os
import time
import ffext
import sys
sys.path.append("./pyproject")

import db.dbs_mgr as db_mgr
import rpc.rpc_def as rpc_def
import dbs_def as dbs_def
import id_manager.idmanager as idmgr_

def ImpDbsCreateUserSession(conn, job):
    session_id = idmgr_.GenPlayerID()
    szAuthKey = job.GetParam()
    sql = "INSERT INTO `account` (`ACCOUNT_ID`, `SESSION_ID`, `SESSION_UPD_TIME`, `CREATE_DATA`) VALUES ('%s', '%s', now(), now()) " % (szAuthKey, session_id)
    job.SetSession(session_id)
    conn.query(sql, db_mgr.OnOneDbQueryDone, job)

def ImpDbsLoadPlayerData(conn, job):
    dictSerial = {
        dbs_def.FLAG: True,
    }
    session = job.GetSession()
    sql = "SELECT NAME, SEX FROM `player` WHERE `SESSION_ID` = '%s' " % (session)
    ret = conn.sync_query(sql)
    if ret.flag is False:
        ffext.ERROR('load_player载入数据出错%s' % (sql))
        dictSerial[dbs_def.FLAG] = False
        db_mgr.OnOneDbQueryDone(dictSerial, job)
        return

    dictRet = {}
    if len(ret.result) == 0:
        sql = "INSERT INTO `player` (`SESSION_ID`, `NAME` , `SEX`, `CREATE_DATA`) VALUES ('%s', '%s', %d, now())" % (session, "_{0}".format(str(session)[:8]), 0)
        ret = conn.sync_query(sql)
        assert ret.flag is True

        dictRet["name"] = "_{0}".format(session)
        dictRet["sex"] = 0
    else:
        dictRet["name"] = ret.result[0][0]
        dictRet["sex"] = ret.result[0][1]

    sql = "SELECT MONEY_TYPE, MONEY_VALUE FROM `player_money` WHERE `SESSION_ID` = '%s' " % (session)
    ret = conn.sync_query(sql)
    if ret.flag is False:
        ffext.ERROR('load_player载入数据出错%s' % (sql))
        dictSerial[dbs_def.FLAG] = False
        db_mgr.OnOneDbQueryDone(dictSerial, job)
        return

    dictRet["money"] = []
    dictSerial[dbs_def.RESULT] = dictRet
    db_mgr.OnOneDbQueryDone(dictSerial, job)
