# -*- coding: utf-8 -*-

g_dictAllEntity = {} # session 2 entityid

def AddEntity(session, entity):
    global g_dictAllEntity
    assert session not in g_dictAllEntity
    g_dictAllEntity[session] = entity

def DelEntity(session):
    global g_dictAllEntity
    if session in g_dictAllEntity:
        g_dictAllEntity.pop(session)

def GetEntity(session):
    return g_dictAllEntity.get(session)

def PlayerOffline(nPlayerGID):
    Player = GetEntity(nPlayerGID)
    assert Player is not None