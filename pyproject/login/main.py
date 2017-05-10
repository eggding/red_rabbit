# coding=UTF-8
import os
import time
import ffext
import event_bus

import sys
sys.path.append("./pyproject")

import rpc.rpc_def as rpc_def
import login.login_mgr as login_mgr

@ffext.reg_service(rpc_def.OnDbsStartUp)
def OnDbsStartUp(dictSerial):
    pass
