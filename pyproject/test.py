# -*- coding:utf-8 -*-

def XiPai():
    import random
    nMaxCarNum = 10
    listTmp = []
    for i in xrange(1, nMaxCarNum + 1):
        listTmp.append(i)

    nLen = nMaxCarNum - 1
    while nLen > 0:
        nPos = random.randint(0, nLen)
        nTmpVal = listTmp[nLen]
        listTmp[nLen] = listTmp[nPos]
        listTmp[nPos] = nTmpVal
        nLen -= 1


for i in xrange(1, 10):
    XiPai()