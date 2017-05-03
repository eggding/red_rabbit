# -*- coding:utf-8 -*-

    bCanNextTurn = gas_mj_event_mgr.TouchEvent(self, EMjEvent.ev_qi_pai, [nPos, nCardID])
  File "./pyproject/gas/gas_mj/gas_mj_event_mgr.py", line 25, in TouchEvent
    return funOpt(mjMgr, evData)
  File "./pyproject/gas/gas_mj/gas_mj_event_mgr.py", line 109, in TouchEventQiPai
    if check_hu_mgr.testGang(nCard, listCardEx, listJinPai) is True:
  File "./pyproject/gas/gas_mj/check_hu.py", line 575, in testGang
    sptArr = seprateArr( tmpArr, hunMj )
  File "./pyproject/gas/gas_mj/check_hu.py", line 241, in seprateArr
    reArr[t].append( mj )
IndexError: list index out of range
