# -*- coding:utf-8 -*-

def IsRobot(nPlayerGID):
    if nPlayerGID < 1000:
        return True
    return False

def IsGasScene(szScene):
    return True if szScene.find("gas") != -1 else False

def IsDbQueue(szScene):
    return True if szScene.find("db") != -1 else False

def dict_merge(dictSrc, dictDst):
    """
    字典合并, dictSrc合并到dictDst
    字典value可以相加
    @param dictDst:
    @param dictSrc:
    @return:
    """
    for keyObj, nData in dictSrc.iteritems():
        if keyObj not in dictDst:
            dictDst[keyObj] = nData
        else:
            dictDst[keyObj] += nData
