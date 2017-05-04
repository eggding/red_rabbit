# -*- coding: utf-8 -*-
# @Author  : jh.feng

import socket
import struct, time
import random

def PacketLoginBuff():
    import proto.login_pb2 as login_pb2
    req_login = login_pb2.login_req()
    global szMsg
    szMsg = "acc" + str(random.randint(1, 99999))
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
    # req.cfg.avg = 0
    szRet = req.SerializeToString()

    # 计算protobol消息体的字节数
    szFormat = "%ds" % len(szRet)
    nTotalSize = struct.calcsize(szFormat)

    # 二进制化消息包
    # 包头(32bit,16bit,16bit) + 包体(Protocol数据)
    szFormat = "IHH%ds" % len(szRet)
    return struct.pack(szFormat, nTotalSize, 10010, 0, szRet)


szCode = """
Player.m_PlayerMoneyMgr.AddMoney(1, 200, "gm test add money")
"""


def PacketExeCode():
    d = {"0": szCode}

    import json
    szAuthCode = json.dumps(d)

    # 计算protobol消息体的字节数
    szFormat = "%ds" % len(szAuthCode)
    nTotalSize = struct.calcsize(szFormat)

    # 二进制化消息包
    # 包头(32bit,16bit,16bit) + 包体(Protocol数据)
    szFormat = "IHH%ds" % len(szAuthCode)
    return struct.pack(szFormat, nTotalSize, 10900, 0, szAuthCode)


c = 0
import random
while True:
    sock = socket.create_connection(("192.168.74.130", 10242))
    # sock = socket.create_connection(("127.0.0.1", 10242))
    sock.send(PacketLoginBuff())
    print(sock.recv(93939))
    # syn scene
    print(sock.recv(93939))

    sock.send(PacketExeCode())
    print("send exe code done.")

    # time.sleep(0.3)
    sock.send(PacketCreateRoomBuff())

    # time.sleep(1)
    # sock.send(PacketExeCode())
    # print("send exe code done.")


    while True:
        print(sock.recv(3948))
        time.sleep(1)

    time.sleep(9939)

    sock.close()
    print("c ", c)
    c += 1

