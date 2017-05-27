# -*- coding: utf-8 -*-
# @Author  : jh.feng

import socket
import struct, time
import random

def PacketLoginBuff():
    import proto.login_pb2 as login_pb2
    req_login = login_pb2.login_req()
    global szMsg
    szMsg = "acc_0"#  +  str(random.randint(1, 1000000000))
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
    req.cfg.opt = 2
    req.cfg.avg = 0
    szRet = req.SerializeToString()

    # 计算protobol消息体的字节数
    szFormat = "%ds" % len(szRet)
    nTotalSize = struct.calcsize(szFormat)

    # 二进制化消息包
    # 包头(32bit,16bit,16bit) + 包体(Protocol数据)
    szFormat = "IHH%ds" % len(szRet)
    return struct.pack(szFormat, nTotalSize, 10010, 0, szRet)

def PacketHeartBreat():
    import proto.common_info_pb2 as common_info_pb2
    rsp = common_info_pb2.heart_beat_req()
    szRet = rsp.SerializeToString()

    # 计算protobol消息体的字节数
    szFormat = "%ds" % len(szRet)
    nTotalSize = struct.calcsize(szFormat)

    # 二进制化消息包
    # 包头(32bit,16bit,16bit) + 包体(Protocol数据)
    szFormat = "IHH%ds" % len(szRet)
    return struct.pack(szFormat, nTotalSize, 10000, 0, szRet)

def PacketAllDone():
    import proto.common_info_pb2 as common_info_pb2
    req = common_info_pb2.client_load_done_req()
    szRet = req.SerializeToString()

    # 计算protobol消息体的字节数
    szFormat = "%ds" % len(szRet)
    nTotalSize = struct.calcsize(szFormat)

    # 二进制化消息包
    # 包头(32bit,16bit,16bit) + 包体(Protocol数据)
    szFormat = "IHH%ds" % len(szRet)
    return struct.pack(szFormat, nTotalSize, 10045, 0, szRet)


def PacketReady():
    import proto.opt_pb2 as opt_pb2
    req = opt_pb2.game_ready_req()
    szRet = req.SerializeToString()

    # 计算protobol消息体的字节数
    szFormat = "%ds" % len(szRet)
    nTotalSize = struct.calcsize(szFormat)

    # 二进制化消息包
    # 包头(32bit,16bit,16bit) + 包体(Protocol数据)
    szFormat = "IHH%ds" % len(szRet)
    return struct.pack(szFormat, nTotalSize, 10043, 0, szRet)


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

def StartUp():
    c = 0
    import random
    while True:
        # sock = socket.create_connection(("112.74.124.100", 10242))
        # sock = socket.create_connection(("192.168.74.130", 10242))
        sock = socket.create_connection(("127.0.0.1", 10242))
        sock.send(PacketLoginBuff())
        print(sock.recv(93939))
        # # syn scene
        print(sock.recv(93939))

        sock.send(PacketExeCode())
        print("send exe code done.")

        # time.sleep(0.3)
        sock.send(PacketCreateRoomBuff())
        time.sleep(5)

        sock.send(PacketAllDone())

        # time.sleep(1)
        # sock.send(PacketExeCode())
        # print("send exe code done.")

        c = 1
        while True:
            # print(sock.recv(3948))
            sock.send(PacketReady())
            t = sock.recv(39484)
            print(t)
            time.sleep(0.5)

            # if c % 5 == 0:

            if c % 10 == 0:
                sock.send(PacketHeartBreat())

        time.sleep(9939)

        sock.close()
        print("c ", c)
        c += 1

if __name__ == "__main__":
    StartUp()
