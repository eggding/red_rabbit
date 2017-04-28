# -*- coding: utf-8 -*-

# 开放给客户端的协议 10001 - 20000
GacRequsetLogin = 10001
Gac2GasChangeScene = 10002
Gac2GasQueryRoomScene = 10003
Gac2GasCreateRoom = 10010
Gac2GasEnterRoom = 10011

ResponseLogin = 20001
Gas2GacRetChangeScene = 20002
Gas2GacretQueryRoomScene = 20003

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

Gcc2GasPlayerOffline = 3000
Gcc2GasRetGenRoomID = 3001
Gcc2GasRetGetRoomScene = 3002
Gcc2GasRetSynPlayerState = 3003

DbsGetUserSession = 7000
DbsLoadPlayerData = 7001
DbsCreateUserSession = 7002
DbsTest = 7003

# 持久化玩家数据
DbsPersistentPlayerData = 7004
DbsGetRoomIDSector = 7005

OnDbAsynCallReturn = 8001