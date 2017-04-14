# -*- coding: utf-8 -*-

# 开放给客户端的协议 10001 - 20000
GacRequsetLogin = 10001
Gac2RoomServiceCreateCreateRoom = 10002
Gac2RoomServiceGetEcho = 10003
Gac2RoomServiceQueryAll = 10004

# 主动同步给客户端的协议 30001 - 32000
ResponseLogin = 30001
SynSceneInfo = 30002
SynPlayerData = 30003

# 内部协议1-8011
OnPlayerOffline = 1

DbsGetUserSession = 7000
DbsLoadPlayerData = 7001
DbsCreateUserSession = 7002
DbsTest = 7003
OnDbAsynCallReturn = 8001