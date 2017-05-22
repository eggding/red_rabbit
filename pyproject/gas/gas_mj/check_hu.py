#coding:utf8

# 数据格式:类型=value/100, 数值=value%10
# [111-119] 万
# [121-129]
# [131-139]
# [141-149]

# [211-219] 筒
# [221-229]
# [231-239]
# [241-249]

# [311-319] 索
# [321-329]
# [331-339]
# [341-349]

# [411-417] 东西南北中发白
# [421-427]
# [431-437]
# [441-447]

# [511-518] 春、夏、秋、冬，梅、兰、竹、菊

# global callTime
from util.enum_def import EMjEvent

callTime = 0

import random
g_NeedHunCount = 4
g_mjsArr = [
    101, 102, 103, 104, 105, 106, 107, 108, 109, #万
    101, 102, 103, 104, 105, 106, 107, 108, 109,
    101, 102, 103, 104, 105, 106, 107, 108, 109,
    101, 102, 103, 104, 105, 106, 107, 108, 109,
    201, 202, 203, 204, 205, 206, 207, 208, 209, #筒
    201, 202, 203, 204, 205, 206, 207, 208, 209,
    201, 202, 203, 204, 205, 206, 207, 208, 209,
    201, 202, 203, 204, 205, 206, 207, 208, 209,
    301, 302, 303, 304, 305, 306, 307, 308, 309, #索
    301, 302, 303, 304, 305, 306, 307, 308, 309,
    301, 302, 303, 304, 305, 306, 307, 308, 309,
    301, 302, 303, 304, 305, 306, 307, 308, 309,
    401, 402, 403, 404, 405, 406, 407, # 东 西 南 北 中 发 白
    401, 402, 403, 404, 405, 406, 407,
    401, 402, 403, 404, 405, 406, 407,
    401, 402, 403, 404, 405, 406, 407,
    501, 502, 503, 504, 505, 506, 507, 508, # 春、夏、秋、冬，梅、兰、竹、菊
] # end

majmap = {"101":"一万","102":"二万","103":"三万","104":"四万","105":"五万","106":"六万","107":"七万","108":"八万","109":"九万",
          "201":"一筒","202":"二筒","203":"三筒","204":"四筒","205":"五筒","206":"六筒","207":"七筒","208":"八筒","209":"九筒",
          "301":"一索","302":"二索","303":"三索","304":"四索","305":"五索","306":"六索","307":"七索","308":"八索","309":"九索",
          "401":"东风","402":"西风","403":"南风","404":"北风","405":"红中","406":"发财","407":"白板",
          "501": "春", "502": "夏", "503": "秋", "504": "冬", "505": "梅", "506": "兰", "507": "竹", "508": "菊"}

listShiSanYao = [101, 109, 201, 209, 301, 309, 401, 402, 403, 404, 405, 406, 407]

def IsBaiBan(nCard):
    return 407 == nCard

def IsHuaPai(nCard):
    return GetCardType(nCard) == 5

def GetBaiBanCard():
    return 407

def GetCardType(nCard):
    return nCard / 100

def GetCardValue(nCard):
    return nCard % 10

def GetCardNameChinese(nCard):
    return majmap.get(str(nCard))

def GenCardArr():
    import copy
    return copy.copy(g_mjsArr)

def GetCardNum():
    return len(g_mjsArr)

# [ 测试使用
g_testMjsArr = [
    101, 101, 101, 101, 102, 102, 104, 201, 103,
    103, 103, 103, 104, 104, 102, 104, 105, 105,
    105, 105, 106, 106, 106, 106, 107, 107, 107,
    107, 108, 108, 108, 108, 109, 109, 109, 109,
    201, 202, 203, 204, 204, 202, 203, 205, 201,
    202, 203, 204, 201, 202, 203, 204, 205, 206,
    207, 208, 206, 102, 207, 208, 205, 206, 207,
    208, 205, 206, 207, 208, 209, 209, 209, 209,
    301, 302, 303, 304, 301, 302, 303, 304, 301,
    302, 303, 304, 301, 302, 303, 304, 305, 306,
    307, 308, 305, 306, 307, 308, 305, 306, 307,
    308, 305, 306, 307, 308, 309, 309, 309, 309,
    401, 402, 403, 404, 405, 406, 407, # 东 西 南 北 中 发 白
    401, 402, 403, 404, 405, 406, 407,
    401, 402, 403, 404, 405, 406, 407,
    401, 402, 403, 404, 405, 406, 407
]
def getTestMjs():
    mjArr = []
    mjArr.extend(g_testMjsArr)
    return mjArr
# 测试使用 ]

# 获得一副牌并混乱牌
def randomMjs():
    mjArr = []
    mjArr.extend(g_mjsArr)
    i = random.randint(1, 5 )
    while i > 0:
        random.shuffle( mjArr )
        i = i - 1
    return mjArr

# 判断是否有效
def isValidMj( mj ):
    itype = mj / 100
    clr = mj % 100 / 10 # 忽略该字段，仅用于判别有效
    value = mj % 10
    if itype == 1 or itype == 2 or itype == 3:
        if value < 1 or value > 9 or clr != 0:
            return False
        else:
            return True
    elif itype == 4:
        if value < 1 or value > 7 or clr != 0:
            return False
        else:
            return True
    else:
        return False

# 获得混
def getHunMj(fanMj):
    t = fanMj / 100
    v = fanMj % 10
    if t == 4:
        v = v+1
        if v > 7:
            v = 1
    elif t>0 and t<5:
        v = v+1
        if v > 9:
            v = 1
    return t*100 + v

def sortArr(arr):
    if len(arr) == 0:
        return
    arr.sort( None, key=lambda v:v%10 )

listCombRet = []
listHunMjTmp = []

def GetAllBaiBanComb(nUsedNum, nTotalNum, listOrder):
    global listHunMjTmp, listCombRet
    if nUsedNum == nTotalNum:
        listCombRet.append(listOrder)
        return

    for mj in listHunMjTmp:
        listTmp = listOrder[:]
        listTmp.append(mj)
        GetAllBaiBanComb(nUsedNum + 1, nTotalNum, listTmp)

def seprateArrAllCombBaiBan( mjArr, hunMj ):
    assert isinstance(hunMj, list)
    reArr = [[],[],[],[],[]]

    listHunMj = []
    for h in hunMj:
        ht = h / 100
        hv = h % 10
        listHunMj.append((ht, hv))

    for mj in mjArr:
        t = mj / 100
        v = mj % 10
        if (t, v) in listHunMj:
            t = 0
        # if ht == t and hv == v:
        #     t = 0
        reArr[t].append( mj )
        sortArr( reArr[t] )

    global listCombRet, listHunMjTmp
    listCombRet = []
    listHunMjTmp = hunMj
    nNumBaiBan = mjArr.count(GetBaiBanCard())
    GetAllBaiBanComb(0, nNumBaiBan, [])

    listRet = [reArr]
    nMjBaiBan = GetBaiBanCard()
    nBaiBanType = GetCardType(nMjBaiBan)
    import copy
    for listOneOrder in listCombRet:
        tmpArr = copy.deepcopy(reArr)

        while True:
            if nMjBaiBan in tmpArr[nBaiBanType]:
                tmpArr[nBaiBanType].remove(nMjBaiBan)
            else:
                break

        listSordID = []
        for mj in listOneOrder:
            tmpArr[GetCardType(mj)].append(mj)
            if GetCardType(mj) not in listSordID:
                listSordID.append(GetCardType(mj))

        for id in listSordID:
            sortArr(tmpArr[id])

        listRet.append(tmpArr)

    return listRet

def seprateArr( mjArr, hunMj ):
    reArr = [[],[],[],[],[]]
    listHunMj = []
    if isinstance(hunMj, list):
        for h in hunMj:
            ht = h / 100
            hv = h % 10
            listHunMj.append((ht, hv))
    else:
        ht = hunMj / 100
        hv = hunMj % 10
        listHunMj.append((ht, hv))

    for mj in mjArr:
        t = mj / 100
        v = mj % 10
        if (t, v) in listHunMj:
            t = 0
        # if ht == t and hv == v:
        #     t = 0
        reArr[t].append( mj )
        sortArr( reArr[t] )

    return reArr

def test3Combine( mj1, mj2, mj3 ):
    t1, t2, t3 = mj1/100, mj2/100, mj3/100
    # 牌型不同不能组合
    if t1 != t2 or t1 != t3:
        return False
    v1, v2, v3 = mj1%10, mj2%10, mj3%10
    # 重牌
    if v1 == v2 and v1 == v3:
        return True
    if t3 == 4:
        return False
    if (v1+1) == v2 and (v1+2) == v3:
        return True
    return False


def getModNeedNum(arrLem,isJiang):
    if arrLem <=0:
        return 0
    modNum = arrLem % 3
    needNumArr = [0,2,1]
    if isJiang:
        needNumArr = [2,1,0]
    return needNumArr[modNum]

def getNeedHunInSub( subArr, hNum ):
    global callTime
    callTime += 1

    global g_NeedHunCount
    if g_NeedHunCount == 0:
        return

    lArr = len(subArr)

    if hNum + getModNeedNum(lArr,False) >= g_NeedHunCount:
        return

    if lArr == 0:
        g_NeedHunCount = min( hNum, g_NeedHunCount )
        return
    elif lArr == 1:
        g_NeedHunCount = min( hNum+2, g_NeedHunCount )
        return
    elif lArr == 2:
        t = subArr[0] / 100
        v0 = subArr[0] % 10
        v1 = subArr[1] % 10
        if t == 4: # 东南西北中发白（无顺）
            if v0 == v1:
                g_NeedHunCount = min( hNum+1, g_NeedHunCount )
                return
        elif  (v1-v0) < 3:
            g_NeedHunCount = min( hNum+1, g_NeedHunCount )
        return
    elif lArr >= 3: # 大于三张牌
        t  = subArr[0] / 100
        v0 = subArr[0] % 10
        v2 = subArr[2] % 10

        #第一个和另外两个一铺
        arrLen = len(subArr)
        for i in range( 1, arrLen ):
            if hNum + getModNeedNum(lArr-3,False)  >= g_NeedHunCount:
                break
            v1 = subArr[i] % 10
            #13444   134不可能连一起
            if v1 - v0 > 1:
                break
            if ( i+2 )  < arrLen:
                if ( subArr[i+2]%10 ) == v1:
                    continue
            if i+1 < arrLen:
                tmp1, tmp2, tmp3 = subArr[0],subArr[i], subArr[i+1]
                if test3Combine( tmp1, tmp2, tmp3 ):
                    subArr.remove( tmp1 )
                    subArr.remove( tmp2 )
                    subArr.remove( tmp3 )
                    subLen = len(subArr)
                    getNeedHunInSub(subArr, hNum)
                    subArr.append( tmp1 )
                    subArr.append( tmp2 )
                    subArr.append( tmp3 )
                    sortArr( subArr )

        # 第一个和第二个一铺
        v1 = subArr[1] % 10
        if hNum + getModNeedNum(lArr-2,False) +1 < g_NeedHunCount:
            if t == 4: # 东南西北中发白（无顺）
                if v0 == v1:
                    tmp1 = subArr[0]
                    tmp2 = subArr[1]
                    subArr.remove( tmp1 )
                    subArr.remove( tmp2 )
                    getNeedHunInSub(subArr, hNum+1)
                    subArr.append( tmp1 )
                    subArr.append( tmp2 )
                    sortArr( subArr )

            else:
                arrLen= len(subArr)
                for i in range( 1, arrLen ):
                    if hNum + getModNeedNum(lArr-2,False) +1  >= g_NeedHunCount:
                        break;
                    v1 = subArr[i] % 10
                    #如果当前的value不等于下一个value则和下一个结合避免重复
                    if (i+1) != arrLen:
                        v2 = subArr[i+1] % 10
                        if v1 == v2:
                            continue
                    mius = v1 - v0
                    if  mius < 3:
                        tmp1 = subArr[0]
                        tmp2 = subArr[i]
                        subArr.remove( tmp1 )
                        subArr.remove( tmp2 )
                        getNeedHunInSub(subArr, hNum+1)
                        subArr.append( tmp1 )
                        subArr.append( tmp2 )
                        sortArr( subArr )
                        if mius >= 1:
                            break
                    else:
                        break

        # 第一个自己一铺
        if  hNum + getModNeedNum(lArr-1,False)+2 < g_NeedHunCount:
            tmp = subArr[0]
            subArr.remove( tmp )
            getNeedHunInSub( subArr, hNum+2 )
            subArr.append( tmp )
            sortArr( subArr )
    else:
        return

def test2Combine( mj1, mj2 ):
    t1, t2 = mj1 / 100, mj2 / 100
    v1, v2 = mj1 % 10, mj2 % 10
    if t1 == t2 and v1 == v2:
        return True
    return False

def canHu( hunNum, arr ):
    global g_NeedHunCount
    tmpArr = []
    tmpArr.extend(arr)
    arrLen  = len( tmpArr )
    if arrLen <= 0:
        if hunNum >= 2:
            return True
        return False

    if hunNum < getModNeedNum(arrLen,True):
        return False

    for i in range( arrLen ):
        if i == (arrLen - 1 ):# 如果是最后一张牌
            if hunNum > 0:
                tmp = tmpArr[i]
                hunNum = hunNum - 1
                tmpArr.remove( tmpArr[i] )
                g_NeedHunCount = 4
                getNeedHunInSub(tmpArr, 0)
                if g_NeedHunCount <= hunNum:
                    # print 'type:',tmp/100, 'value', tmp%10, 1
                    return True
                hunNum = hunNum +1
                tmpArr.append(tmp)
                sortArr(tmpArr)
        else:
            if ( i+2 ) == arrLen or (tmpArr[i]%10) != (tmpArr[i+2]%10):
                if test2Combine( tmpArr[i], tmpArr[i+1] ):
                    tmp1 = tmpArr[i]
                    tmp2 = tmpArr[i+1]
                    tmpArr.remove( tmp1 )
                    tmpArr.remove( tmp2 )
                    g_NeedHunCount = 4
                    getNeedHunInSub(tmpArr, 0)
                    if g_NeedHunCount <= hunNum:
                        # print 'type:',tmp1/100, 'value', tmp1%10, 2
                        return True
                    tmpArr.append( tmp1 )
                    tmpArr.append( tmp2 )
                    sortArr(tmpArr)
            if hunNum>0 and (tmpArr[i]%10) != (tmpArr[i+1]%10):
                hunNum = hunNum -1
                tmp = tmpArr[i]
                tmpArr.remove( tmp )
                g_NeedHunCount = 4
                getNeedHunInSub(tmpArr, 0)
                if g_NeedHunCount <= hunNum:
                    # print 'type:',tmp/100, 'value', tmp%10, 3
                    return True
                hunNum = hunNum +1
                tmpArr.append( tmp )
                sortArr( tmpArr )
    return False

def GetHuType(mjArr, hunMj):
    if CheckIsQiDuiZi(mjArr, hunMj) is True:
        return EMjEvent.ev_hu_qi_dui_zi

    if CheckShiSanYao(mjArr, hunMj) is True:
        return EMjEvent.ev_hu_shi_san_yao

    if CheckDanYou(mjArr, hunMj) is True:
        return EMjEvent.ev_dan_you

    return EMjEvent.ev_hu_normal

def CheckDanYou(listMj, listHunMj):
    reArr = seprateArr(listMj, listHunMj)
    if 2 != len(reArr[0]):
        return False
    for i in xrange(1, 5):
        if 0 == len(reArr[i]):
            continue
        if 3 != len(reArr[i]):
            return False

        if reArr[i][0] + 1 == reArr[i][1] and reArr[i][1] + 1 == reArr[i][2]:
            # a, a+1, a+2
            pass
        elif reArr[i][0] == reArr[i][1] and reArr[i][1] == reArr[i][2]:
            # a, a, a
            pass
        else:
            return False
    return True

def CheckShiSanYao(listMj, listHunMj):
    if len(listMj) != 14:
        return False

    nHunNum = 0
    dictExist = {}
    for mj in listMj:
        if mj in listHunMj:
            nHunNum += 1
        else:
            dictExist[mj] = dictExist.get(mj, 0) + 1

    if len(dictExist) != len(listMj) - nHunNum:
        return False

    global listShiSanYao
    nRequireNum = 0
    for mj in listShiSanYao:
        if mj not in dictExist:
            nRequireNum += 1

    if nRequireNum > nHunNum:
        return False

    return True

def CheckSanJinDao(listMj, listHunMj):
    if 1 != len(listHunMj):
        return False
    if 3 != listMj.count(listHunMj[0]):
        return False
    return True

def CheckIsQiDuiZi(listMj, listHunMj):
    if len(listMj) != 14:
        return False

    nHunNum = 0
    dictExist = {}
    for mj in listMj:
        if mj in listHunMj:
            nHunNum += 1
        else:
            dictExist[mj] = dictExist.get(mj, 0) + 1

    for mj, nCount in dictExist.iteritems():
        if nCount % 2 == 0:
            continue
        nHunNum -= 1

    if nHunNum < 0:
        return False

    return True

def CheckBaXianGuoHai(listMj):
    nNum = 0
    for mj in listMj:
        if GetCardType(mj) == 5:
            nNum += 1
    return nNum == 8

# 判断胡牌
def testHu( mj, mjArr, hunMj ):

    global g_NeedHunCount
    global callTime
    callTime = 0
    tmpArr = []
    tmpArr.extend(mjArr) # 创建一个麻将数组的copy
    if mj != 0:
        tmpArr.append( mj ) # 插入一个麻将

    if CheckIsQiDuiZi(tmpArr, hunMj) is True:
        return True

    if CheckShiSanYao(tmpArr, hunMj) is True:
        return True

    listTmpRet = seprateArrAllCombBaiBan(tmpArr, hunMj)
    for sptArr in listTmpRet:
        # sptArr = seprateArr( tmpArr, hunMj )
        curHunNum = len( sptArr[0] )
        if curHunNum > 3:
            return True

        ndHunArr = [] # 每个分类需要混的数组
        for i in range( 1, 5 ):
            g_NeedHunCount = 4
            getNeedHunInSub( sptArr[i], 0 )
            ndHunArr.append(g_NeedHunCount)
        isHu = False
        # 将在万中
        #如果需要的混小于等于当前的则计算将在将在万中需要的混的个数
        ndHunAll = ndHunArr[1] + ndHunArr[2] + ndHunArr[3]
        if ndHunAll <= curHunNum:
            hasNum = curHunNum - ndHunAll
            isHu = canHu( hasNum, sptArr[1] )
            if isHu:
                return True
        # 将在筒中
        ndHunAll = ndHunArr[0] + ndHunArr[2] + ndHunArr[3]
        if ndHunAll <= curHunNum:
            hasNum = curHunNum - ndHunAll
            isHu = canHu( hasNum, sptArr[2] )
            if isHu:
                return True
        # 将在索中
        ndHunAll = ndHunArr[0] + ndHunArr[1] + ndHunArr[3]
        if ndHunAll <= curHunNum:
            hasNum = curHunNum - ndHunAll
            isHu = canHu( hasNum, sptArr[3] )
            if isHu:
                return True
        # 将在风中
        ndHunAll = ndHunArr[0] + ndHunArr[1] + ndHunArr[2]
        if ndHunAll <= curHunNum:
            hasNum = curHunNum - ndHunAll
            isHu = canHu( hasNum, sptArr[4] )
            if isHu:
                return True
    return False

def testGang( mj, mjArr, hunMj ):
    t = mj / 100
    v = mj % 10
    c = 0
    tmpArr = []
    for tmj in mjArr:
        if 5 == GetCardType(tmj):
            continue
        else:
            tmpArr.append(tmj)
    # tmpArr.extend(mjArr)
    sptArr = seprateArr( tmpArr, hunMj )
    if len( sptArr[t] ) < 2:
        return False
    else:
        for tmj in sptArr[t]:
            if ( tmj%10 ) == v:
                c = c+1
        if c == 3:
            return True

        return False

def testPeng( mj, mjArr, hunMj ):
    t = mj / 100
    v = mj % 10
    c = 0
    tmpArr = []
    tmpArr.extend(mjArr)
    sptArr = seprateArr( tmpArr, hunMj )
    if len( sptArr[t] ) < 2:
        return False
    else:
        for tmj in sptArr[t]:
            if ( tmj%10 ) == v:
                c = c+1
        if c == 2 or c == 3:
            return True

def analyzeAnGang( mjArr, hunMj ):
    result = []
    tmpArr = []
    tmpArr.extend(mjArr)
    sptArr = seprateArr( tmpArr, hunMj )
    for i in range(len(sptArr)):
        subLen = len( sptArr[i] )
        if subLen < 4:
            continue
        else:
            for j in range(subLen):
                if ( subLen - 1 - j )<3:
                    break
                if (sptArr[i][j]%10) == (sptArr[i][j+1]%10) and \
                                (sptArr[i][j+1]%10) == (sptArr[i][j+2]%10) and \
                                (sptArr[i][j+2]%10) == (sptArr[i][j+3]%10):
                    result.append( sptArr[i][j] )
    return result

def rmSample( mj, mjArr, cnt=0 ):
    i = cnt
    j = 0
    while i>0:
        if mjArr.count( mj ):
            mjArr.remove( mj )
            j += 1
        i -= 1
    return j


def getJiangNeedHum(arr):
    global g_NeedHunCount
    minNeedNum = 4
    tmpArr = []
    tmpArr.extend(arr)
    arrLen  = len( tmpArr )
    if arrLen <= 0:
        return 2
    for i in range( arrLen ):
        if i == (arrLen - 1 ):# 如果是最后一张牌
            tmp = tmpArr[i]

            tmpArr.remove( tmpArr[i] )
            g_NeedHunCount = 4
            getNeedHunInSub(tmpArr, 0)
            minNeedNum = min(minNeedNum,g_NeedHunCount+1)

            tmpArr.append(tmp)
            sortArr(tmpArr)
        else:
            if ( i+2 ) == arrLen or (tmpArr[i]%10) != (tmpArr[i+2]%10):
                if test2Combine( tmpArr[i], tmpArr[i+1] ):
                    tmp1 = tmpArr[i]
                    tmp2 = tmpArr[i+1]
                    tmpArr.remove( tmp1 )
                    tmpArr.remove( tmp2 )
                    g_NeedHunCount = 4
                    getNeedHunInSub(tmpArr, 0)

                    minNeedNum = min(minNeedNum,g_NeedHunCount)

                    tmpArr.append( tmp1 )
                    tmpArr.append( tmp2 )
                    sortArr(tmpArr)
            if (tmpArr[i]%10) != (tmpArr[i+1]%10):


                tmp = tmpArr[i]
                tmpArr.remove( tmp )
                g_NeedHunCount = 4
                getNeedHunInSub(tmpArr, 0)

                minNeedNum = min(minNeedNum,g_NeedHunCount+1)

                tmpArr.append( tmp )
                sortArr( tmpArr )
    return minNeedNum


def getTingArr(mjArr,hunMj):
    global g_NeedHunCount
    global callTime
    tmpArr = []
    tmpArr.extend(mjArr) # 创建一个麻将数组的copy
    listRetArr = seprateArrAllCombBaiBan( tmpArr, hunMj )
    tingArr = []
    for sptArr in listRetArr:

        ndHunArr = [] # 每个分类需要混的数组
        for i in range( 1, 5 ):
            g_NeedHunCount = 4
            getNeedHunInSub( sptArr[i], 0 )
            ndHunArr.append(g_NeedHunCount)


        jaNdHunArr = []#每个将分类需要混的数组
        for i in range(1,5):
            jdNeedHunNum = getJiangNeedHum(sptArr[i])
            jaNdHunArr.append(jdNeedHunNum)


        curHunNum = len( sptArr[0])
        paiArr = [[101,110],[201,210],[301,310],[401,408]]

        #是否单调将
        isAllHu = False
        needNum = 0
        for i in range(0,4):
            needNum += ndHunArr[i]
        if curHunNum - needNum == 1:
            isAllHu = True
        if isAllHu:
            for lis in paiArr:
                for x in range(lis[0],lis[1]):
                    if x not in tingArr:
                        tingArr.append(x)
            return  tingArr


        for i in range(0,4):
            # if len(sptArr[i+1]) == 0:
            #     continue;
            # 听牌是将
            needNum = 0
            for j in range(0,4):
                if(i != j):
                    needNum = needNum + ndHunArr[j]

            if needNum <= curHunNum:
                for k in range(paiArr[i][0],paiArr[i][1]):
                    t = [k]
                    t.extend(sptArr[i+1])
                    sortArr(t)
                    if canHu(curHunNum-needNum,t):
                        if k not in tingArr:
                            tingArr.append(k)
                        # print callTime

            # 听牌是扑
            for j in range(0,4):
                if(i != j):
                    needNum = 0
                    for k in range(0,4):
                        if(k != i):
                            if(k == j):
                                needNum += jaNdHunArr[k]
                            else:
                                needNum += ndHunArr[k]
                    if needNum <= curHunNum:
                        for k in range(paiArr[i][0],paiArr[i][1]):
                            if k not in tingArr:
                                t = [k]
                                t.extend(sptArr[i+1])
                                g_NeedHunCount = 4
                                sortArr(t)
                                getNeedHunInSub(t, 0 )
                                if g_NeedHunCount <= curHunNum - needNum:
                                    tingArr.append(k)

        if(len(tingArr) > 0) and hunMj not in tingArr:
            tingArr.append(hunMj)

    return  tingArr



def getTingNumArr(mjArr,hunMj):
    global g_NeedHunCount
    global callTime
    tmpArr = []
    tmpArr.extend(mjArr) # 创建一个麻将数组的copy
    sptArr = seprateArr( tmpArr, hunMj )

    ndHunArr = [] # 每个分类需要混的数组
    for i in range( 1, 5 ):
        g_NeedHunCount = 4
        getNeedHunInSub( sptArr[i], 0 )
        ndHunArr.append(g_NeedHunCount)


    jaNdHunArr = []#每个将分类需要混的数组
    for i in range(1,5):
        jdNeedHunNum = getJiangNeedHum(sptArr[i])
        jaNdHunArr.append(jdNeedHunNum)

    #给一个混看能不能胡
    curHunNum = len( sptArr[0])+1
    tingArr = []


    #是否单调将
    isAllHu = False
    needNum = 0
    for i in range(0,4):
        needNum += ndHunArr[i]
    if curHunNum - needNum == 1:
        isAllHu = True
    if isAllHu:
        tingArr.extend(tmpArr)
        return  tingArr

    for i in range(0,4):
        setTmp = set(sptArr[i+1])
        for x in setTmp:
            t = []
            t.extend(sptArr[i+1])
            t.remove(x)
            # 将
            needNum = 0
            for j in range(0,4):
                if(i != j):
                    needNum = needNum + ndHunArr[j]
            if needNum <= curHunNum and x not in tingArr:
                if canHu(curHunNum-needNum,t):
                    tingArr.append(x)
            # print callTime

            # 扑
            for j in range(0,4):
                if len(sptArr[j+1]) == 0:
                    continue
                if(i != j):
                    needNum = 0
                    for k in range(0,4):
                        if(k != i):
                            if(k == j):
                                needNum += jaNdHunArr[k]
                            else:
                                needNum += ndHunArr[k]
                    if needNum <= curHunNum and x not in tingArr:
                        g_NeedHunCount = 4
                        getNeedHunInSub(t, 0 )
                        if g_NeedHunCount <= curHunNum - needNum:
                            tingArr.append(x)
                            # print str(callTime) + 10*'-'
    return tingArr


import datetime
# print 'reqOtherAction +2'
# samArr = [111, 111, 111, 111, 214, 214, 214, 214, 315, 315, 315, 315, 118, 119, 119 ]
# begin = datetime.datetime.now()
# print testHu(112, samArr, 111)
# end = datetime.datetime.now()
# print end-begin

# samArr = [405,104,104,107,107,203,204,205,207,105,107,108,109]
# getTingArr(samArr,405)
#testPengGang( 302,samArr, 403 ):
# hasGang( samArr, 115 )
#samArr = [101, 101,101,101,101,101,101,101,101,101,101,101,101,101,101,101,101 ]
#print testGang(101, samArr, 102)


if __name__ == "__main__":
    pass

    # 一万, 一筒, 二筒, 四筒, 四筒, 五筒, 五筒, 六筒, 七筒, 七筒, 九筒, 六索, 九索
    # listMj = [101, 201, 202, 204, 204, 205, 205, 206, 207, 207, 209, 306, 309]
    # testHu(301, listMj, [107, 102])

    # print(len(g_mjsArr))

    #####################################
    #测试胡牌
    # samArr = [111, 111, 111, 111, 214, 214, 214, 214, 315, 315, 315, 315, 118, 119, 119 ]
    # print testHu(112, samArr, 111)
    #####################################


    #####################################
    #测试具体能听哪些牌
    # samArr = [405,202,203,203,204,205,302,302,303,303]#运行时间:0:00:00.001100 <callTime:83>  [ 一筒 , 四筒 , 二索 , 三索 , 红中 , ]
    # samArr = [405,202,203,203,204,205,301,302,303,303]#运行时间:0:00:00.000721 <callTime:72>  [ 一筒 , 四筒 , 三索 , 红中 , ]
    # samArr = [405,202,203,203,204,205,301,302,302,303]#运行时间:0:00:00.000659 <callTime:72>  [ 一筒 , 四筒 , 二索 , 红中 , ]
    # samArr = [405,203,203,204,205,301,302,302,303,303]#运行时间:0:00:00.000887 <callTime:72>  [ 三筒 , 六筒 , 一索 , 四索 , 红中 , ]
    # samArr = [405,202,203,204,205,301,302,302,303,303]#运行时间:0:00:00.000715 <callTime:59>  [ 二筒 , 五筒 , 一索 , 四索 , 红中 , ]
    # samArr = [405,202,203,203,204,301,302,302,303,303]#运行时间:0:00:00.000797 <callTime:72>  [ 三筒 , 一索 , 四索 , 红中 , ]
    # samArr = [405,104,104,107,107,107,203,204,205,305,307,308,309]#运行时间:0:00:00.000791 <callTime:83>  [ 四万 , 五索 , 三索 , 四索 , 六索 , 七索 , 红中 , ]
    # samArr = [405,104,104,107,107,107,203,204,205,207,307,308,309]#运行时间:0:00:00.000844 <callTime:85>  [ 四万 , 七筒 , 二筒 , 五筒 , 六筒 , 八筒 , 九筒 , 红中 , ]
    # samArr = [405,104,105,106,107,108,109,202,202,302,304,306,306]#运行时间:0:00:00.000799 <callTime:88>  [ 二筒 , 三索 , 六索 , 红中 , ]
    # samArr = [405,103,104,105,107,108,109,202,202,302,304,306,306]#运行时间:0:00:00.000859 <callTime:89>  [ 二筒 , 三索 , 六索 , 红中 , ]
    # samArr = [405,103,104,105,106,107,108,202,202,302,304,306,306]#运行时间:0:00:00.000836 <callTime:88>  [ 二筒 , 三索 , 六索 , 红中 , ]
    # #测试两个癞子的运行时间
    # samArr = [405,405,103,105,106,107,108,202,202,302,304,306,306]#运行时间:0:00:00.000955 <callTime:136>  [ 四万 , 二筒 , 三索 , 六索 , 红中 , ]
    # samArr = [405,405,103,105,106,107,108,201,202,302,304,306,306]#运行时间:0:00:00.000696 <callTime:94>  [ 四万 , 三筒 , 三索 , 红中 , ]
    # samArr = [405,405,103,105,106,107,108,201,202,302,303,306,306]#运行时间:0:00:00.000790 <callTime:94>  [ 四万 , 三筒 , 一索 , 四索 , 红中 , ]
    # #测试三个癞子的运行时间
    # samArr = [405,405,405,105,106,107,108,202,202,302,304,306,306]#运行时间:0:00:00.001111 <callTime:135>  [ 五万 , 八万 , 三万 , 四万 , 六万 , 七万 , 九万 , 二筒 , 三索 , 六索 , 红中 , ]
    # samArr = [405,405,405,105,106,107,108,201,202,302,304,306,306]#运行时间:0:00:00.000926 <callTime:118>  [ 五万 , 八万 , 三万 , 四万 , 六万 , 七万 , 九万 , 三筒 , 三索 , 六索 , 红中 , ]
    # samArr = [405,405,405,105,106,107,108,201,202,302,303,306,306]#运行时间:0:00:00.000949 <callTime:116>  [ 五万 , 八万 , 三万 , 四万 , 六万 , 七万 , 九万 , 三筒 , 一索 , 四索 , 六索 , 红中 , ]
    # #测试四个癞子的运行时间
    # samArr = [405,405,405,405,106,107,108,202,202,302,304,306,306]#运行时间:0:00:00.000607 <callTime:18>  [ 一万 , 二万 , 三万 , 四万 , 五万 , 六万 , 七万 , 八万 , 九万 , 一筒 , 二筒 , 三筒 , 四筒 , 五筒 , 六筒 , 七筒 , 八筒 , 九筒 , 一索 , 二索 , 三索 , 四索 , 五索 , 六索 , 七索 , 八索 , 九索 , 东风 , 西风 , 南风 , 北风 , 红中 , 发财 , 白板 , ]
    # samArr = [405,405,405,405,106,107,108,201,202,302,304,306,306]#运行时间:0:00:00.000390 <callTime:18>  [ 一万 , 二万 , 三万 , 四万 , 五万 , 六万 , 七万 , 八万 , 九万 , 一筒 , 二筒 , 三筒 , 四筒 , 五筒 , 六筒 , 七筒 , 八筒 , 九筒 , 一索 , 二索 , 三索 , 四索 , 五索 , 六索 , 七索 , 八索 , 九索 , 东风 , 西风 , 南风 , 北风 , 红中 , 发财 , 白板 , ]
    # samArr = [405,405,405,405,106,107,108,201,202,302,303,306,306]#运行时间:0:00:00.000758 <callTime:18>  [ 一万 , 二万 , 三万 , 四万 , 五万 , 六万 , 七万 , 八万 , 九万 , 一筒 , 二筒 , 三筒 , 四筒 , 五筒 , 六筒 , 七筒 , 八筒 , 九筒 , 一索 , 二索 , 三索 , 四索 , 五索 , 六索 , 七索 , 八索 , 九索 , 东风 , 西风 , 南风 , 北风 , 红中 , 发财 , 白板 , ]
    #####################################

    #####################################
    #测试打出哪些牌能听
    # tingNumArr = [405,202,203,203,204,205,301,302,302,303,303]#运行时间:0:00:00.000704 <callTime:48>  [ 二筒 , 三筒 , 五筒 , 一索 , 二索 , 三索 , ]
    # tingNumArr = [405,104,104,107,107,107,203,204,205,207,305,307,308,309]#运行时间:0:00:00.000649 <callTime:61>  [ 七筒 , 五索 , ]
    # tingNumArr = [405,103,104,105,106,107,108,109,202,202,302,304,306,306]#运行时间:0:00:00.000874 <callTime:82>  [ 三万 , 六万 , 九万 , ]
    # #测试两个癞子
    # tingNumArr = [405,405,203,203,204,205,301,302,302,303,303]#运行时间:0:00:00.000424 <callTime:35>  [ 三筒 , 四筒 , 五筒 , 一索 , 二索 , 三索 , ]
    # tingNumArr = [405,405,104,107,107,107,203,204,205,207,305,307,308,309]#运行时间:0:00:00.000616 <callTime:63>  [ 四万 , 七筒 , 五索 , ]
    # tingNumArr = [405,405,104,105,106,107,108,109,202,202,302,304,306,306]#运行时间:0:00:00.000551 <callTime:48>  [ 四万 , 五万 , 六万 , 七万 , 八万 , 九万 , 二筒 , 四索 , 六索 , 二索 , ]
    # #测试三个癞子
    # tingNumArr = [405,405,405,203,204,205,301,302,302,303,303]#运行时间:0:00:00.000493 <callTime:27>  [ 三筒 , 四筒 , 五筒 , 一索 , 二索 , 三索 , ]
    # tingNumArr = [405,405,405,107,107,107,203,204,205,207,305,307,308,309]#运行时间:0:00:00.000518 <callTime:36>  [ 七万 , 三筒 , 四筒 , 五筒 , 七筒 , 五索 , 七索 , 八索 , 九索 , ]
    # tingNumArr = [405,405,405,105,106,107,108,109,202,202,302,304,306,306]#运行时间:0:00:00.000522 <callTime:53>  [ 五万 , 六万 , 七万 , 八万 , 九万 , 二筒 , 四索 , 六索 , 二索 , ]
    # #测试四个癞子
    # tingNumArr = [405,405,405,405,204,205,301,302,302,303,303]#运行时间:0:00:00.000422 <callTime:24>  [ 四筒 , 五筒 , 一索 , 二索 , 三索 , ]
    # tingNumArr = [405,405,405,405,107,107,203,204,205,207,305,307,308,309]#运行时间:0:00:00.000604 <callTime:35>  [ 七万 , 三筒 , 四筒 , 五筒 , 七筒 , 五索 , 七索 , 八索 , 九索 , ]
    # tingNumArr = [405,405,405,405,106,107,108,109,202,202,302,304,306,306]#运行时间:0:00:00.000678 <callTime:31>  [ 六万 , 七万 , 八万 , 九万 , 二筒 , 四索 , 六索 , 二索 , ]
    # tingNumArr = [407,407,104,105,106,106,306,306,402,402,405,405,406,406]

    ##############################
    # 测试特殊情况  单一花色重复多次
    # tingNumArr = [405,201,201,201,201,202,202,202,202,205,205,205,205,209]#运行时间:0:00:00.006123 <callTime:356>  [ 五筒 , 九筒 , ]
    # tingNumArr = [405,405,202,204,205,205,206,206,207,208,208,208,209,306]#运行时间:0:00:00.002929 <callTime:358>  [ 二筒 , 九筒 , 六索 , ]
    # # samArr = [405,201,201,201,201,201,202,202,202,202,204,204,205]#运行时间:0:00:00.016391 <callTime:1029>  [ 三筒 , 六筒 , 红中 , ]
    # samArr = [405,405,201,201,201,201,202,202,202,202,407,204,407]#运行时间:0:00:00.026671 <callTime:1527>  [ 三筒 , 四筒 , 七筒 , 八筒 , 九筒 , 红中 , ]
    # ##############################
    #
    # global callTime
    # callTime = 0
    # begin = datetime.datetime.now()
    # # 测试摸哪些牌能胡牌
    # tingArr = testHu(0, samArr, [405, 302])
    #测试打哪些牌能听牌
    # tingArr = getTingNumArr(tingNumArr, 405)
    #测试摸到这张牌是不是能胡牌
    # tingArr = {}
    # print testHu(209, samArr, 405)
    # tingArr = []
    # for i in tingNumArr:
    #     tmp = []
    #     tmp.extend(tingNumArr)
    #     tmp.remove(i)
    #     getTingNumArr(tmp,405)

    # end = datetime.datetime.now()
    # runTime = end - begin
    # rstr = "运行时间:" + str(runTime) + " <callTime:" + str(callTime) + ">  [ "
    # for i in range(0,len(tingArr)):
    #     key = str(tingArr[i])
    #     rstr +=  majmap.get(key) + " , "
    # rstr += "]"
    #
    # print  rstr


