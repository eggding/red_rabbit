# -*- coding: utf-8 -*-
# @Author  : jh.feng

class StateBase(object):
    def __init__(self, owner):
        self.m_Owner = None

    def GetOwner(self):
        return self.m_Owner

    def Destroy(self):
        self.OnDestroy()
        self.m_Owner = None

    def OnDestroy(self):
        pass

    def Enter(self):
        self.OnEnter()

    def OnEnter(self):
        pass

class StateMachine(object):
    def __init__(self):
        self.m_CurState = None

    def IsInState(self, state):
        return isinstance(self.m_CurState, state)

    def Destroy(self):
        if self.m_CurState is not None:
            self.m_CurState.Destroy()
        self.m_CurState = None

    def ChangeState(self, newState):
        if self.m_CurState is not None:
            self.m_CurState.Destroy()

        self.m_CurState = newState
        if newState is not None:
            self.m_CurState.Enter()