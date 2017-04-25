# -*- coding: utf-8 -*-

# 开放给客户端的协议 10001 - 20000
GacRequsetLogin = 10001
Gac2RoomServiceCreateRoom = 10002
Gac2RoomServiceEnterRoom = 10003
Gac2RoomServiceQueryAll = 10004

# 主动同步给客户端的协议 30001 - 32000
ResponseLogin = 30001
SynSceneInfo = 30002
SynPlayerData = 30003

# 内部协议1-8011
OnPlayerOffline = 1

GetGateIp = 1001
OnSessionConnectGate = 1002
OnSessionDisConnGate = 1003

Room2MjStartGame = 2001
Room2MjOnRoomMemberEnter = 2002
Room2MjOnRoomMemberOffline = 2003
Logic2RoomServiceGameEnd = 2052

Login2GccPlayerOffline = 1059
Gas2GccSynPlayerGasID = 2060
Gcc2GasPlayerOffline = 3000

DbsGetUserSession = 7000
DbsLoadPlayerData = 7001
DbsCreateUserSession = 7002
DbsTest = 7003

# 持久化玩家数据
DbsPersistentPlayerData = 7004
DbsGetRoomIDSector = 7005

OnDbAsynCallReturn = 8001