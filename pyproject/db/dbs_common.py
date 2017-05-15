# -*- coding:utf-8 -*
import ffext
from util.enum_def import EDbsOptType
import MySQLdb

def Ping(conn):
    print("dbs_common.Ping")
    conn.ping()
    ret = SyncQueryTrans(EDbsOptType.eQuery, conn, "select * from account limit 1")
    print("pint ret ", ret)

def SyncQueryTrans(nType, conn, sql):
    try:
        cur = conn.cursor()
        ret = cur.execute(sql)
        if nType == EDbsOptType.eQuery:
            ret = cur.fetchmany(ret)
        cur.close()
        conn.commit()
        return ret
    except MySQLdb.Error, e:
        conn.rollback()
        try:
            sqlError = "Error %d:%s" % (e.args[0], e.args[1])
        except IndexError:
            sqlError = "MySQL Error:%s" % str(e)
        ffext.ERROR(sqlError)
        return None