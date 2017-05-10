# -*- coding: utf-8 -*-
# @Author  : jh.feng

import sys
import ffext

sys.path.append("./pyproject")
import rpc.rpc_def as rpc_def
import gcc.gcc_scene.gcc_scene_mgr as gcc_scene_mgr
import gcc.gcc_room_mgr.gcc_room_mgr as gcc_room_mgr

@ffext.reg_service(rpc_def.OnDbsStartUp)
def OnDbsStartUp(dictSerial):
    import id_manager.room_id_mgr as room_id_mgr
    room_id_mgr.init()


