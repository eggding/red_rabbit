# coding=UTF-8

import ffext
import sys, json, time
sys.path.append("./pyproject")

import util.util as util
import db.dbs_mgr as db_mgr
import rpc.rpc_def as rpc_def
import dbs_def as dbs_def
import db.table.table_property_def as table_property_def
import id_manager.idmanager as idmgr_

szStartTrans = "START TRANSACTION;"
szCommit = "COMMIT;"
szRollBack = "ROLLBACK;"

def ImpDbsGetRoomIDSector(conn, job):
    nIdBegin, nIDEnd = idmgr_.GenRoomIDSector(conn)
    dictSerial = {dbs_def.FLAG: True,
                  dbs_def.RESULT: [nIdBegin, nIDEnd]}
    db_mgr.OnOneDbQueryDone(dictSerial, job)

def ImpDbsTest(conn, job):
    sql = "SELECT DATA_INFO_BASE FROM player limit 10;"
    conn.query(sql, db_mgr.OnOneDbQueryDone, job)

def ImpGetUserSession(conn, job):
    dictRet = {
        dbs_def.FLAG: True,
    }
    szAuthKey = job.GetParam()
    sql = "select `SESSION_ID` FROM `account` WHERE `ACCOUNT_ID` = '%s'" % (szAuthKey)
    ret = conn.sync_query(sql)

    if ret.flag is False:
        dictRet[dbs_def.FLAG] = False
        db_mgr.OnOneDbQueryDone(dictRet, job)
        return

    print("ret.result", ret.result)
    if len(ret.result) == 0:
        session_id = idmgr_.GenPlayerID(conn)
        # sql = "INSERT INTO `account` VALUES ('%s', '%s', now(), now()) " % (szAuthKey, session_id)
        sql = "INSERT INTO `account` VALUES('%s', '%s', now(), now())" % (szAuthKey, session_id)
        print(sql)
        job.SetSession(session_id)
        ret = conn.sync_query(sql)
        if ret.flag is False:
            dictRet[dbs_def.FLAG] = False
            db_mgr.OnOneDbQueryDone(dictRet, job)
            return

        dictRet[dbs_def.RESULT] = [[session_id]]
    else:
        dictRet[dbs_def.RESULT] = ret.result

    db_mgr.OnOneDbQueryDone(dictRet, job)


def ImpDbsCreateUserSession(conn, job):
    # print("ImpDbsCreateUserSession")
    session_id = idmgr_.GenPlayerID(conn)
    szAuthKey = job.GetParam()
    sql = "INSERT INTO `account` (`ACCOUNT_ID`, `SESSION_ID`, `SESSION_UPD_TIME`, `CREATE_DATA`) VALUES ('%s', '%s', now(), now()) " % (szAuthKey, session_id)
    job.SetSession(session_id)
    # print("start running create user session job ",  session_id, job.GetCbID())
    conn.query(sql, db_mgr.OnOneDbQueryDone, job)


def ImpDbsPersistentPlayerData(conn, job):
    """
    持久化玩家信息
    :param conn:
    :param job:
    :return:
    """
    # sql = "SELECT `player` SET DATA_INFO = '%s' WHERE `SESSION_ID` = '%s'" % (dictSerial, session)
    # sql = "UPDATE player SET DATA_INFO = JSON_SET(DATA_INFO, '$.%s', '%s') where SESSION_ID = '%s'" % (szProperty, json.dumps(valueObj), session)
    dictSerial = job.GetParam()
    session = job.GetSession()
    sql = "UPDATE player SET DATA_INFO = '%s' where SESSION_ID = '%s'" % (dictSerial.encode("utf-8"), session)
    conn.query(sql, db_mgr.OnOneDbQueryDone, job)

def ImpDbsLoadPlayerData(conn, job):
    dictSerial = {
        dbs_def.FLAG: True,
    }
    session = job.GetSession()
    sql = "SELECT DATA_INFO_BASE, DATA_INFO FROM `player` WHERE `SESSION_ID` = '%s'" % (session)
    ret = conn.sync_query(sql)
    if ret.flag is False:
        ffext.ERROR('load_player载入数据出错%s' % (sql))
        dictSerial[dbs_def.FLAG] = False
        db_mgr.OnOneDbQueryDone(dictSerial, job)
        return

    if len(ret.result) == 0:
        dictPlayerInfo = {
            table_property_def.Player.SESSION_ID: session,
            table_property_def.Player.NAME: "name_" + str(session),
            table_property_def.Player.SEX: session % 2,
            table_property_def.Player.CREATE_TIME: int(time.time()),
        }
        szDataInfo = json.dumps(dictPlayerInfo)
        szExtraInfo = json.dumps({table_property_def.Player.MONEY_LIST: []})
        sql = "INSERT INTO `player` VALUES('%s', '%s', '%s')" % (session, szDataInfo, szExtraInfo)
        ret = conn.sync_query(sql)
        if ret.flag is False:
            ffext.ERROR('load_player载入数据出错%s' % (sql))
            dictSerial[dbs_def.FLAG] = False
            db_mgr.OnOneDbQueryDone(dictSerial, job)
            return
    else:
        szPlayerInfoBase = ret.result[0][0]
        szPlayerInfoExtra = ret.result[0][1]
        dictPlayerInfo = json.loads(szPlayerInfoBase)
        dictTmp = json.loads(szPlayerInfoExtra)
        print(szPlayerInfoExtra)
        util.dict_merge(dictTmp, dictPlayerInfo)


    dictSerial[dbs_def.RESULT] = dictPlayerInfo
    db_mgr.OnOneDbQueryDone(dictSerial, job)
