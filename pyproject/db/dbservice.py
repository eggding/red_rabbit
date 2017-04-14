# -*- coding: utf-8 -*-

import ffext

table_num = 1

g_sync_db = None
g_async_db = None

szDbName = "red_rabbit"
szMysqlPwd = "pascalx64"

def init():
    pass

def get_sync_db():
    global g_sync_db
    if None == g_sync_db:
        g_sync_db = ffext.ffdb_create('mysql://localhost:3306/root/{0}/{1}'.format(szMysqlPwd, szDbName))
    return g_sync_db

def get_async_db():
    global g_async_db
    if None == g_async_db:
        g_async_db = ffext.ffdb_create('mysql://localhost:3306/root/{0}/{1}'.format(szMysqlPwd, szDbName))
    return g_async_db

def format_player_table(player):
    return 'account'

def get_session_by_auth_key(szAuthKey):
    sql = "select `SESSION_ID` FROM `account` WHERE `ACCOUNT_ID` = '%s'" % (szAuthKey)
    ret = get_sync_db().sync_query(sql)
    if ret.flag is False:
        return 0
    if len(ret.result) == 0:
        import id_manager.idmanager as idmgr_
        session_id = idmgr_.GenPlayerID(get_sync_db())
        sql = "INSERT INTO `account` (`ACCOUNT_ID`, `SESSION_ID`, `SESSION_UPD_TIME`, `CREATE_DATA`) VALUES ('%s', '%s', now(), now()) " % (szAuthKey, session_id)
        ret = get_sync_db().sync_query(sql)
        assert ret.flag is True
        return session_id
    else:
        return int(ret.result[0][0])

def register_player(player):
    sql = "INSERT INTO `player_register` (`NAME` , `PASSWORD`) VALUES ('%s', '%s') " % (player.nick_name, player.password)
    ret = get_sync_db().sync_query(sql)
    if ret.flag == False:
        print('账号已存在，注册失败:%s'%(sql))
        return False
    verify_password(player)
    return init_player_db(player)


def init_player_db(player):
    sql = "INSERT INTO `%s` (`ID`, `REAL_NAME` , `NICK_NAME`, `EMAIL`, `LEVEL`, `EXP`, `EXTRA_DATA`) VALUES ('%s', '%s', '%s', '%s', '%d', '%d', '%s') "\
          ""% (format_player_table(player), player.id(), player.real_name, player.nick_name, player.email, player.level, player.exp, player.get_extra_data())
    ret = get_sync_db().sync_query(sql)
    if ret.flag == False:
        print('账号初始化失败:%s'%(sql))
        return False
    return True

def verify_password(player):
    sql = "select `ID` FROM `player_register` WHERE `NAME` = '%s' AND `PASSWORD` = '%s'" % (player.nick_name, player.password)
    ret = get_sync_db().sync_query(sql)
    if len(ret.result) == 0:
        ffext.ERROR('verify_password无此账号[%s]'%(sql))
        return False
    player.set_id(int(ret.result[0][0]))
    return True

def load_player(session, callback):
    dictRet = {"session": session}
    sql = "SELECT NAME, SEX FROM `player` WHERE `SESSION_ID` = '%s' " % (session)
    print("sql ", sql)
    ret = get_sync_db().sync_query(sql)
    if ret.flag is False:
        ffext.ERROR('load_player载入数据出错%s' % (sql))
        return

    if len(ret.result) == 0:
        sql = "INSERT INTO `player` (`SESSION_ID`, `NAME` , `SEX`, `CREATE_DATA`) VALUES ('%s', '%s', %d, now())" % (session, "_{0}".format(str(session)[:8]), 0)
        print("cereate new ", sql)
        ret = get_sync_db().sync_query(sql)
        assert ret.flag is True

        dictRet["name"] = "_{0}".format(session)
        dictRet["sex"] = 0
    else:
        dictRet["name"] = ret.result[0][0]
        dictRet["sex"] = ret.result[0][1]

    sql = "SELECT MONEY_TYPE, MONEY_VALUE FROM `player_money` WHERE `SESSION_ID` = '%s' " % (session)
    ret = get_sync_db().sync_query(sql)
    if ret.flag is False:
        ffext.ERROR('load_player载入数据出错%s' % (sql))
        return

    dictRet["money"] = []
    callback(dictRet)

    # def cb(ret):
    #     print("on cb ", ret)
    #     if ret.flag == False or len(ret.result) == 0:
    #         ffext.ERROR('load_player载入数据出错%s'%(sql))
    #         return
    #     ret.dump()
    #     callback(ret.result)
    # get_async_db().query(sql, cb)
