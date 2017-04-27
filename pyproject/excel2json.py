# -*- coding: utf-8 -*-

import sys
import xlrd
import json

file = "./cfg_excel/score.xls"

data = xlrd.open_workbook(file)
table=data.sheets()[0]
nrows=table.nrows
ncols = table.ncols

dictRet = {}
listKeys = table.row_values(0)
for i in xrange(1, nrows):
    dictRet[i] = {}
    listRowValues = table.row_values(i)
    for nPos, szKey in enumerate(listKeys):
        szKey = szKey.encode("utf-8")
        dictRet[listRowValues[0]][szKey] = listRowValues[nPos]

print(dictRet)
print(dictRet[2]["类型"])