# -*- coding: utf-8 -*-
# @Author  : jh.feng

import ffext
import sys, json, time
sys.path.append("./pyproject")

import util.util as util
import dbs_def as dbs_def
import db.table.table_property_def as table_property_def
from util.enum_def import EDbsOptType
import dbs_common as dbs_common
import id_manager.player_id_mgr as player_id_mgr

def ImpGetIDData(conn, job):
    dictRet = {dbs_def.FLAG: True}
    nTypeID, nServerID = job.GetParam()
    sql = "SELECT `AUTO_INC_ID`, `RUNING_FLAG` FROM `id_generator` WHERE `TYPE` = '%d' AND `SERVER_ID` = '%d'" % (nTypeID, nServerID)
    ret = dbs_common.SyncQueryTrans(EDbsOptType.eQuery, conn, sql)
    if len(ret) == 0:
        # 数据库中还没有这一行，插入
        sql = "INSERT INTO `id_generator` SET `AUTO_INC_ID` = '0',`TYPE` = '%d', `SERVER_ID` = '%d', `RUNING_FLAG` = '1' " % (nTypeID, nServerID)
        assert dbs_common.SyncQueryTrans(EDbsOptType.eInsert, conn, sql) is not None
        dictRet[dbs_def.RESULT] = [0, 1]
        return dictRet

    sql = "UPDATE `id_generator` SET `RUNING_FLAG` = '1' WHERE `TYPE` = '%d' AND `SERVER_ID` = '%d'" % (nTypeID, nServerID)
    assert dbs_common.SyncQueryTrans(EDbsOptType.eUpdate, conn, sql) is not None
    dictRet[dbs_def.RESULT] = ret[0]
    return dictRet

def ImpUpdateID(conn, job):
    now_val, type_id, server_id, now_val = job.GetParam()
    sql = "UPDATE `id_generator` SET `AUTO_INC_ID` = '%d' WHERE `TYPE` = '%d' AND `SERVER_ID` = '%d' AND `AUTO_INC_ID` < '%d'" % (now_val, type_id, server_id, now_val)
    assert dbs_common.SyncQueryTrans(EDbsOptType.eUpdate, conn, sql) is not None
    dictSerial = {dbs_def.FLAG: True}
    # db_mgr.OnOneDbQueryDone(dictSerial, job)
    return dictSerial

def ImpDbsTest(conn, job):
    assert False
    # sql = "SELECT DATA_INFO_BASE FROM player limit 10;"
    # conn.query(sql, db_mgr.OnOneDbQueryDone, job)

def ImpDbsSaveAllGmConfig(conn, job):
    dictRet = {
        dbs_def.FLAG: True,
    }
    szData = job.GetParam()
    sql = "select * FROM `game_config` limit 1"
    ret = dbs_common.SyncQueryTrans(EDbsOptType.eQuery, conn, sql)
    if ret is None:
        dictRet[dbs_def.FLAG] = False
        return dictRet

    if len(ret) == 0:
        sql = "INSERT INTO `game_config` VALUES('%s', '%s')" % (1, szData)
    else:
        sql = "UPDATE `game_config` SET CONFIG_DATA = '%s' where CONFIG_ID = '%s'" % (szData.encode("utf-8"), 1)

    ret = dbs_common.SyncQueryTrans(EDbsOptType.eQuery, conn, sql)
    if ret is None:
        dictRet[dbs_def.FLAG] = False
        return dictRet

    dictRet[dbs_def.RESULT] = ret
    return dictRet

def ImpGetAllGmConfig(conn, job):
    dictRet = {
        dbs_def.FLAG: True,
    }
    sql = "select * FROM `game_config` limit 1"
    ret = dbs_common.SyncQueryTrans(EDbsOptType.eQuery, conn, sql)
    if ret is None:
        dictRet[dbs_def.FLAG] = False
        return dictRet

    dictRet[dbs_def.RESULT] = ret
    return dictRet

def ImpGetUserSession(conn, job):
    dictRet = {
        dbs_def.FLAG: True,
    }
    szAuthKey = job.GetParam()
    sql = "select `SESSION_ID` FROM `account` WHERE `ACCOUNT_ID` = '%s'" % (szAuthKey)
    ret = dbs_common.SyncQueryTrans(EDbsOptType.eQuery, conn, sql)
    if ret is None:
        dictRet[dbs_def.FLAG] = False
        return dictRet

    if len(ret) == 0:
        session_id = player_id_mgr.GenPlayerID(conn)
        sql = "INSERT INTO `account` VALUES('%s', '%s', now(), now())" % (szAuthKey, session_id)
        job.SetSession(session_id)
        ret = dbs_common.SyncQueryTrans(EDbsOptType.eInsert, conn, sql)
        if ret is None:
            ffext.ERROR('create session err %s' % (sql))
            dictRet[dbs_def.FLAG] = False
            return dictRet

        dictRet[dbs_def.RESULT] = session_id
    else:
        dictRet[dbs_def.RESULT] = ret[0][0]

    return dictRet

def ImpDbsCreateUserSession(conn, job):
    print("ImpDbsCreateUserSession")
    # session_id = idmgr_.GenPlayerID(conn)
    # szAuthKey = job.GetParam()
    # sql = "INSERT INTO `account` (`ACCOUNT_ID`, `SESSION_ID`, `SESSION_UPD_TIME`, `CREATE_DATA`) VALUES ('%s', '%s', now(), now()) " % (szAuthKey, session_id)
    # job.SetSession(session_id)
    # # print("start running create user session job ",  session_id, job.GetCbID())
    # conn.query(sql, db_mgr.OnOneDbQueryDone, job)


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
    dbs_common.SyncQueryTrans(EDbsOptType.eUpdate, conn, sql)
    dictSerial = {
        dbs_def.FLAG: True
    }
    return dictSerial

def ImpDbsLoadPlayerData(conn, job):
    dictSerial = {
        dbs_def.FLAG: True,
    }
    session = job.GetSession()
    sql = "SELECT DATA_INFO_BASE, DATA_INFO FROM `player` WHERE `SESSION_ID` = '%s'" % (session)
    ret = dbs_common.SyncQueryTrans(EDbsOptType.eQuery, conn, sql)
    if ret is None:
        ffext.ERROR('load_player载入数据出错%s' % (sql))
        dictSerial[dbs_def.FLAG] = False
        return dictSerial

    if len(ret) == 0:
        dictPlayerInfo = {
            table_property_def.Player.SESSION_ID: session,
            table_property_def.Player.NAME: "name_" + str(session),
            table_property_def.Player.SEX: session % 2,
            table_property_def.Player.CREATE_TIME: int(time.time()),
        }
        szDataInfo = json.dumps(dictPlayerInfo)
        szExtraInfo = json.dumps({table_property_def.Player.MONEY_LIST: []})
        sql = "INSERT INTO `player` VALUES('%s', '%s', '%s')" % (session, szDataInfo, szExtraInfo)
        ret = dbs_common.SyncQueryTrans(EDbsOptType.eInsert, conn, sql)
        if ret is None:
            ffext.ERROR('load_player载入数据出错%s' % (sql))
            dictSerial[dbs_def.FLAG] = False
            return dictSerial
    else:
        szPlayerInfoBase = ret[0][0]
        szPlayerInfoExtra = ret[0][1]
        dictPlayerInfo = json.loads(szPlayerInfoBase)
        dictTmp = json.loads(szPlayerInfoExtra)
        util.dict_merge(dictTmp, dictPlayerInfo)

    dictSerial[dbs_def.RESULT] = dictPlayerInfo
    return dictSerial
