# -*- coding: utf-8 -*-
# @Author  : jmhuo

import os
import time
import xupdate as ModXupdate
import framework.app as ModApp

g_dLastModifyTime = {}  #szFilePath:time


def Init():
    import platform
    import framework.app as ModApp

    if 'Windows' == platform.system():
        if (ModApp.GetApp().IsGds() or ModApp.GetApp().IsGam() or ModApp.GetApp().IsLgs() or ModApp.GetApp().IsUCServer() ) and ModApp.GetApp().CanAutoReload():
            ModApp.GetLogger().info("Enable Auto Reload.")
            import framework.tick_mgr as ModTickMgr
            ModTickMgr.RegisterNotFixTick("reload tick", 1000, OnUpdate)
    else:
        if ModApp.GetApp().CanAutoReload():
            ModApp.GetLogger().info("Enable Auto Reload.")
            import framework.tick_mgr as ModTickMgr
            ModTickMgr.RegisterNotFixTick("reload tick", 1000, OnUpdate)


def CheckFileAndUpdate(szFilePath):
    import os
    fileName = os.path.basename(os.path.splitext(szFilePath)[0])

    bNeedUpdate = False
    global g_dLastModifyTime

    nModifyTime = os.stat(szFilePath).st_mtime

    if g_dLastModifyTime.get(szFilePath,theApp.GetStartTimeStamp())<nModifyTime:
        bNeedUpdate = True
        g_dLastModifyTime[szFilePath] = nModifyTime

    if bNeedUpdate:
        import sys
        #print ("auto reload:" , fileName)
        for k, v in sys.modules.iteritems():
            tmpFileName = k.split('.')[-1]
            if fileName == tmpFileName:
                if v:
                    ModXupdate.update(k)

    return bNeedUpdate


def OnReloadedSomeFile():
    import platform
    import framework.app as ModApp
    if ('Windows' == platform.system() and ModApp.GetApp().IsGam()):
        ModApp.GetApp().ReloadAllFileOnAllAnyServer()

def LookRoundTheFiles(szPath):

    bNeedUpdate=False

    for szBaseDir, lDirList, lFileList in os.walk(szPath):
        for szFileName in lFileList:
            if not szFileName.endswith(".py"):
                continue

            szFilePath = os.path.join(szBaseDir, szFileName)
            bNeedUpdate = bNeedUpdate or CheckFileAndUpdate(szFilePath)

    if bNeedUpdate:
        OnReloadedSomeFile()

def OnUpdate():

    try:
        pathlist=ModApp.GetApp().GetReloadPath()
        if pathlist:
            for i in pathlist :
                #print i
                LookRoundTheFiles(i)
    except Exception, e:
        ModApp.GetApp().GetLogger().error("%s",e)
