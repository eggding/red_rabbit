# -*- coding: utf-8 -*-
# @Author  : jh.feng

import ffext

def RegisterOnceTick(nMs, funObj, param=None):
    return ffext.once_timer(nMs, funObj, param)

def UnRegisterOnceTick(nTickID):
    ffext.cancel_timer(nTickID)