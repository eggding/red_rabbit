# -*- coding:utf-8 -*-
import socket
import struct, time

sock = socket.create_connection(("112.74.124.100", 10242))

def PacketLoginBuff():
    szAuthCode = "pascal"

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
    return struct.pack(szFormat, nTotalSize, 10001, 0, szAuthCode)

def SendEcho():
    szAuthCode = "hi"

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
    return struct.pack(szFormat, nTotalSize, 30002, 0, szAuthCode)

sock.send(PacketLoginBuff())
print(sock.recv(3844))

while True:
    print(sock.recv(4949))
