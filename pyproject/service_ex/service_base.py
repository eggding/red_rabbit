# -*- coding: utf-8 -*-
# @Author  : jh.feng

import ff
import ffext
import rpc.rpc_def as rpc_def
import util.tick_mgr as tick_mgr

g_szServiceMgr = "service_mgr"

def ServiceCheckTick():
    tick_mgr.RegisterOnceTick(10000, ServiceCheckTick)
    ffext.call_service(g_szServiceMgr, 0, "test")

def Connect2ExService():
    import conf as conf
    conn_info = conf.dict_cfg[g_szServiceMgr]["conn_info"]
    szAddr, szPort = conn_info.split(":")
    ret = ffext.connect_to_outer_service(g_szServiceMgr, "tcp://{0}:{1}".format(szAddr, szPort))
    print("Connect2ExService", ret)
    assert 0 == ret

@ffext.reg_service(rpc_def.ServiceExRsp)
def ServiceExRsp(dictSerial):
    print("test service on ", ff.service_name)
    print(dictSerial)

Connect2ExService()
