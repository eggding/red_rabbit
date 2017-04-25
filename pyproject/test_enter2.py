# -*- coding: utf-8 -*-
# @Author  : jh.feng
# -*- coding:utf-8 -*-
import socket
import struct, time

def PacketLoginBuff():
    import proto.login_pb2 as login_pb2
    req_login = login_pb2.request_login()
    global szMsg
    szMsg = "acc2"
    req_login.auth_info = szMsg
    szMsg = req_login.SerializeToString()

    # 计算protobol消息体的字节数
    szFormat = "%ds" % len(szMsg)
    nTotalSize = struct.calcsize(szFormat)

    # 二进制化消息包
    # 包头(32bit,16bit,16bit) + 包体(Protocol数据)
    szFormat = "IHH%ds" % len(szMsg)
    return struct.pack(szFormat, nTotalSize, 10001, 0, szMsg)

def PacketEnterRoomBuff():
    szAuthCode = "aa"

    import proto.login_pb2 as login_pb2
    req_login = login_pb2.request_login()
    req_login.auth_info = szAuthCode
    szAuthCode = req_login.SerializeToString()

    # 计算protobol消息体的字节数
    szFormat = "%ds" % len(szAuthCode)
    nTotalSize = struct.calcsize(szFormat)

    # 二进制化消息包
    # 包头(32bit,16bit,16bit) + 包体(Protocol数据)
    szFormat = "IHH%ds" % len(szAuthCode)
    return struct.pack(szFormat, nTotalSize, 10003, 0, szAuthCode)

while True:
    sock = socket.create_connection(("192.168.74.130", 10242))
    # sock = socket.create_connection(("127.0.0.1", 10242))
    sock.send(PacketLoginBuff())
    print(sock.recv(93939))

    time.sleep(0.2)
    sock.send(PacketEnterRoomBuff())

    time.sleep(9939)

    sock.close()
