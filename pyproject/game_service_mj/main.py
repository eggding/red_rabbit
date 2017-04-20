# -*- coding: utf-8 -*-
# @Author  : jh.feng

import ffext
import sys, json
sys.path.append("./pyproject")

import rpc.rpc_def as rpc_def

@ffext.reg_service(rpc_def.OnPlayerOffline)
def OnPlayerOffline(session):
    ffext.LOGINFO("FFSCENE_PYTHON", "RoomCenter player offline {0}".format(session))
    session = session["0"]
    return {"ret": True}