# -*- coding: utf-8 -*-

import sys
import xlrd
import json
import pprint, cStringIO

szPath = "./pyproject/cfg_excel/"
szSaveDir = "./pyproject/cfg_py/"

# szPath = "./cfg_excel/"
# szSaveDir = "./cfg_py/"


listFile = [
    "parameter_common",
]

class UniPrinter(pprint.PrettyPrinter):
    def format(self, obj, context, maxlevels, level):
        if isinstance(obj, unicode):
            out = cStringIO.StringIO()
            out.write('u"')
            for c in obj:
                if ord(c)<32 or c in u'"\\':
                    out.write('\\x%.2x' % ord(c))
                else:
                    out.write(c.encode("utf-8"))

            out.write('"')
            # result, readable, recursive
            return out.getvalue(), True, False
        elif isinstance(obj, str):
            out = cStringIO.StringIO()
            out.write('"')
            for c in obj:
                if ord(c)<32 or c in '"\\':
                    out.write('\\x%.2x' % ord(c))
                else:
                    out.write(c)

            out.write('"')
            # result, readable, recursive
            return out.getvalue(), True, False
        else:
            return pprint.PrettyPrinter.format(self, obj,
                context,
                maxlevels,
                level)

def SaveCfgJson(szFileName, dictData):
    # 创建下载目录
    global szSaveDir
    szSavePath = szSaveDir + szFileName + ".py"
    import os
    if not os.path.exists(szSaveDir):
        os.makedirs(szSaveDir)
    try:
        with open(szSavePath, 'wb') as file_write:
            file_write.write(r"# -*- coding: utf-8 -*-")
            file_write.write("\n\n")
            ret = "{0} = {1}".format(szFileName, UniPrinter().pformat(dictData))
            file_write.write(ret)
    except:
        assert False

def ConverXlsxToJson(szFile):
    data = xlrd.open_workbook(szFile)
    table=data.sheets()[0]
    nrows=table.nrows

    dictRet = {}
    listKeys = table.row_values(0)
    for i in xrange(1, nrows):
        dictRet[i] = {}
        listRowValues = table.row_values(i)
        for nPos, szKey in enumerate(listKeys):
            szKey = szKey.encode("utf-8")

            v = listRowValues[nPos]
            if isinstance(v, str) or isinstance(v, unicode):
                pass
            else:
                v = str(listRowValues[nPos])
                if v.find(".") != -1:
                    tmp = v.split(".")[1]
                    if int(tmp) != 0:
                        v = listRowValues[nPos]
                    else:
                        v = int(listRowValues[nPos])
                else:
                    v = int(listRowValues[nPos])

            dictRet[int(listRowValues[0])][szKey] = v

    return dictRet

def LoadAllCfg():
    import os
    print(os.getcwd())
    for szCfg in listFile:
        szFile = szPath + szCfg + ".xlsx"
        dictTmp = ConverXlsxToJson(szFile)
        SaveCfgJson(szCfg, dictTmp)
