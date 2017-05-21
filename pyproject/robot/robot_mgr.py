# -*- coding: utf-8 -*-
# @Author  : jh.feng

import ff, ffext
import random
import util.tick_mgr as tick_mgr
import entity.entity_mgr as entity_mgr

class RobotMgr(object):
    def __init__(self):
        import conf as conf
        nRobotNum = conf.dict_cfg["gas"]["robot_num"]
        self.m_nRobotStartID = (int(ff.service_name[-1:]) + 1) * 100

        self.m_dictRobotGID = {}
        import gas.gas_scene.gas_scene_mgr as gas_scene_mgr
        for i in xrange(1, nRobotNum + 1):
            import json
            dict = {"ip": "127.0.0.1", "gate": "gate@0"}
            gas_scene_mgr._gasSceneMgr.Gcc2GasSessionConn(self.m_nRobotStartID, json.dumps(dict))
            self.m_dictRobotGID[self.m_nRobotStartID] = False
            self.m_nRobotStartID += 1

        ffext.LOGINFO("FFSCENE_PYTHON", "RobotMgr.CreateRobot {0} done.".format(nRobotNum))

        for nGID in self.m_dictRobotGID.keys():
            tick_mgr.RegisterOnceTick(5 * 1000, self.CheckEnterRoom, nGID)

    def CheckEnterRoom(self, nGID):
        t = random.randint(10, 70)
        t = int((t / 10.0) * 1000)
        tick_mgr.RegisterOnceTick(t, self.CheckEnterRoom, nGID)

        robotEntity = entity_mgr.GetEntity(nGID)
        assert robotEntity is not None
        if robotEntity.GetRoomID() is not None:
            return
        self.Try2EnterRoom(nGID)

    def Try2EnterRoom(self, nGID):
        import gas.gas_room_mgr.gas_room_mgr as gas_room_mgr
        gas_room_mgr.EnterRoom(nGID, 0)
        gas_room_mgr.MemberReady(nGID)

_robotMgr = RobotMgr()
