# -*- coding:utf-8 -*-
import socket
import struct, time

import random
szMsg = "pas_______{0}".format(random.randint(1, 104994))

def PacketLoginBuff():
    import proto.login_pb2 as login_pb2
    req_login = login_pb2.login_req()
    global szMsg
    szMsg = "acc"
    req_login.type = login_pb2.login_type.Value("login")
    req_login.auth_info = szMsg
    szMsg = req_login.SerializeToString()

    # 计算protobol消息体的字节数
    szFormat = "%ds" % len(szMsg)
    nTotalSize = struct.calcsize(szFormat)

    # 二进制化消息包
    # 包头(32bit,16bit,16bit) + 包体(Protocol数据)
    szFormat = "IHH%ds" % len(szMsg)
    return struct.pack(szFormat, nTotalSize, 10001, 0, szMsg)

def PacketCreateRoomBuff():
    import proto.create_room_pb2 as create_room_pb2
    req = create_room_pb2.create_room_req()
    req.game_type = 1
    req.cfg.member_num = 4
    req.cfg.multi = 5
    req.cfg.total_start_game_num = 5
    req.cfg.opt = 1
    szRet = req.SerializeToString()

    # 计算protobol消息体的字节数
    szFormat = "%ds" % len(szRet)
    nTotalSize = struct.calcsize(szFormat)

    # 二进制化消息包
    # 包头(32bit,16bit,16bit) + 包体(Protocol数据)
    szFormat = "IHH%ds" % len(szRet)
    return struct.pack(szFormat, nTotalSize, 10010, 0, szRet)

c = 0
import random
while True:
    sock = socket.create_connection(("192.168.74.130", 10242))
    # sock = socket.create_connection(("127.0.0.1", 10242))
    sock.send(PacketLoginBuff())
    print(sock.recv(93939))

    time.sleep(0.1)
    sock.send(PacketCreateRoomBuff())
    #
    time.sleep(9939)

    sock.close()
    print("c ", c)
    c += 1

