# -*- coding:utf-8 -*-

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
