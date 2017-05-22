# -*- coding: utf-8 -*-

# 开放给客户端的协议 10001 - 20000
GacHeartBreat = 10000
GacRequsetLogin = 10001
Gac2GasChangeScene = 10002
Gac2GasQueryRoomScene = 10003
Gac2GasCreateRoom = 10010
Gac2GasEnterRoom = 10011
Gac2GasExitRoom = 10015
Gac2GasOptMj = 10021

Gac2GasGameReady = 10043

Gac2GasQueryGameConf = 10050
Gac2GasOptGameConf = 10051
Gac2GasExeCode = 10900

RspHeartBreat = 20000
ResponseLogin = 20001
Gas2GacRetChangeScene = 20002
Gas2GacretQueryRoomScene = 20003
Gas2GacRetCreateRoom = 20010
Gas2GacRetEnterRoom = 20011
Gas2GacSynGameRet = 20012
Gas2GacOnTouchGameEvent = 20013
Gas2GacRspSynGameData = 20014
Gas2GacRetExitRoom = 20015
Gas2GacOnTouchMemberEvent = 20019
Gas2GacRspOpt = 20021
Gas2GacSynCardInfo = 20041
Gac2GasSynGameOrder = 20042
Gac2GasRetGameReady = 20043
Gas2GacSynAllConfig = 20050
Gas2GacRetModifyConfig = 20051
Gas2GacRetShowResultOne = 20061
Gas2GacRetShowResultAll = 20062
Gas2GacRetStartNewRound = 20063
Gas2GacRetSynMemberState = 20064

SynSceneInfo = 30002
SynPlayerData = 30003

# 内部协议1-8011
OnPlayerOffline = 1

GetGateIp = 1001
OnSessionConnectGate = 1002
OnSessionDisConnGate = 1003

Login2GccPlayerOffline = 1059
Gas2GccSynPlayerGasID = 2060
Gas2GccPlayerTrueOffline = 2061
Gas2GccGenRoomID = 2062
Gas2GccGetRoomSceneByRoomID = 2063
Gas2GccOnRoomDismiss = 2064
Gas2GccStartGameOnRoom = 2065
Gas2GccQueryGmConfig = 2066
Gas2GccModifyGmConfig = 2067

Gcc2GasPlayerOffline = 3000
Gcc2GasRetGenRoomID = 3001
Gcc2GasRetGetRoomScene = 3002
Gcc2GasRetSynPlayerState = 3003

All2ExeCode = 4000

DbsGetUserSession = 7000
DbsLoadPlayerData = 7001
DbsCreateUserSession = 7002
DbsTest = 7003

# 持久化玩家数据
DbsPersistentPlayerData = 7004
DbsGetRoomIDSector = 7005
DbsGetIDData = 7006
DbsUpdateID = 7007
DbsQueueStartUp = 7008
DbsGetAllGmConfig = 7009
DbsSaveAllGmConfig = 7010

OnDbAsynCallReturn = 8001
OnAllServiceStartUp = 8002
OnServiceConn = 8003

TestService = 8999

Peer = 9000
RspPeer = 9001