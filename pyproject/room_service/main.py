# coding=UTF-8
import ffext
import sys, json
sys.path.append("./pyproject")

import rpc.rpc_def as rpc_def
import room_service.room_mgr as room_mgr
import db.dbs_client as dbs_client

import proto.login_pb2 as login_pb2
@ffext.session_call(rpc_def.Gac2RoomServiceQueryAll, login_pb2.request_login)
def Gac2RoomServiceQueryAll(session, dictData):
    def OnDbsTestCb(ret):
        ffext.send_msg_session(session, 344, ret)

    dbs_client.DoAsynCall(rpc_def.DbsTest, session, 0, OnDbsTestCb, nChannel=session)

@ffext.reg_service(rpc_def.OnPlayerOffline)
def OnPlayerOffline(session):
    ffext.LOGINFO("FFSCENE_PYTHON", "RoomCenter player offline {0}".format(session))
    session = session["0"]
    room_mgr.OnPlayerLeaveScene(session)
    return {"ret": True}