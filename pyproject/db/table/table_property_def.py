# -*- coding:utf-8 -*-

class Const(object):
    class ConstError(TypeError):
        pass

    def __setattr__(self, name, value):
        if self.__dict__.has_key(name):
            raise self.ConstError, "Can't rebind const(%s)" % name
        self.__dict__[name] = value

class MemoryAttr(Const):
    GATE = "g"
    IP = "ip"
    ONLINE_TIME = "ot"

# 表名称定义
class Player(Const):
     SESSION_ID = "SESSION_ID"
