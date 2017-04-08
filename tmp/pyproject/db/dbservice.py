# -*- coding: utf-8 -*-

import ffext

table_num = 1

g_sync_db = None
g_async_db = None
def init():
    pass

def get_sync_db():
    global g_sync_db
    if None == g_sync_db:
        g_sync_db = ffext.ffdb_create('mysql://localhost:3306/root/pascalx64/red_rabbit')
    return g_sync_db

def get_async_db():
    global g_async_db
    if None == g_async_db:
        g_async_db = ffext.ffdb_create('mysql://localhost:3306/root/pascalx64/red_rabbit')
    return g_async_db

def format_player_table(player):
    return 'account'

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

def load_player(player, callback):
    sql = "SELECT * FROM `%s`  WHERE `ACCOUNT_ID` = '%s' " % (format_player_table(player), player.id())
    def cb(ret):
        print("on cb ", ret)
        if ret.flag == False or len(ret.result) == 0:
            ffext.ERROR('load_player载入数据出错%s'%(sql))
            return
        ret.dump()
        callback()
    get_async_db().query(sql, cb)
    return True
