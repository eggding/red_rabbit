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

def ImpDbsTest(conn, job):
    sql = "SELECT DATA_INFO_BASE FROM player limit 10;"
    conn.query(sql, db_mgr.OnOneDbQueryDone, job)

def ImpGetUserSession(conn, job):
    szAuthKey = job.GetParam()
    sql = "select `SESSION_ID` FROM `account` WHERE `ACCOUNT_ID` = '%s'" % (szAuthKey)
    conn.query(sql, db_mgr.OnOneDbQueryDone, job)

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
    dictSerial = job.GetParam()
    session = job.GetSession()
    # sql = "SELECT `player` SET DATA_INFO = '%s' WHERE `SESSION_ID` = '%s'" % (dictSerial, session)
    # sql = "UPDATE player SET DATA_INFO = JSON_SET(DATA_INFO, '$.%s', '%s') where SESSION_ID = '%s'" % (szProperty, json.dumps(valueObj), session)
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
        sql = "INSERT INTO `player` VALUES('%s', '%s', '%s')" % (session, szDataInfo, "{}")
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
        dictTmp = json.load(szPlayerInfoExtra)
        util.dict_merge(dictTmp, dictPlayerInfo)


    dictSerial[dbs_def.RESULT] = dictPlayerInfo
    db_mgr.OnOneDbQueryDone(dictSerial, job)

    # INSERT INTO player VALUES (21474928788, {"create_time": 1492604398.771422, "name": "name 21474928788", "SESSION_ID": 21474928788, "sex": 0});

    # sql = "SELECT NAME, SEX FROM `player` WHERE `SESSION_ID` = '%s' " % (session)
    # ret = conn.sync_query(sql)
    # if ret.flag is False:
    #     ffext.ERROR('load_player载入数据出错%s' % (sql))
    #     dictSerial[dbs_def.FLAG] = False
    #     db_mgr.OnOneDbQueryDone(dictSerial, job)
    #     return
    #
    # dictRet = {}
    # if len(ret.result) == 0:
    #     sql = "INSERT INTO `player` (`SESSION_ID`, `NAME` , `SEX`, `CREATE_DATA`) VALUES ('%s', '%s', %d, now())" % (session, "_{0}".format(str(session)[:8]), 0)
    #     ret = conn.sync_query(sql)
    #     if ret.flag is False:
    #         dictSerial[dbs_def.FLAG] = False
    #         db_mgr.OnOneDbQueryDone(dictSerial, job)
    #         return
    #
    #     dictRet[table_property_def.Player.SESSION_ID] = "_{0}".format(session)
    #     dictRet[table_property_def.Player.NAME] = "_{0}".format(str(session)[:8])
    #     dictRet[table_property_def.Player.SEX] = 0
    # else:
    #     dictRet[table_property_def.Player.SESSION_ID] = ret.result[0][0]
    #     dictRet[table_property_def.Player.NAME] = ret.result[0][1]
    #     dictRet[table_property_def.Player.SEX] = ret.result[0][2]
    #
    # sql = "SELECT MONEY_TYPE, MONEY_VALUE FROM `player_money` WHERE `SESSION_ID` = '%s' " % (session)
    # ret = conn.sync_query(sql)
    # if ret.flag is False:
    #     ffext.ERROR('load_player载入数据出错%s' % (sql))
    #     dictSerial[dbs_def.FLAG] = False
    #     db_mgr.OnOneDbQueryDone(dictSerial, job)
    #     return
    #
    # listMoney = []
    # for listOneRet in ret.result:
    #     listMoney.append((listOneRet[0], listOneRet[1]))

