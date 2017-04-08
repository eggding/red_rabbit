# -*- coding:utf-8 -*-
import socket

sock = socket.create_connection(("127.0.0.1", 10242))
# sock = socket.create_connection(("112.74.124.100", 10341))
# protocol 消息
szMsg = "pascal"

# 计算protobol消息体的字节数
import struct, time
szFormat = "%ds" % len(szMsg)
nTotalSize = struct.calcsize(szFormat)

# 二进制化消息包
# 包头(32bit,16bit,16bit) + 包体(Protocol数据)
szFormat = "IHH%ds" % len(szMsg)
buffer = struct.pack(szFormat, nTotalSize, 238, 0, szMsg)
sock.send(buffer)
print(sock.recv(3844))
#
# # 计算protobol消息体的字节数
# szMsg = "hel"
# szFormat = "%ds" % len(szMsg)
# nTotalSize = struct.calcsize(szFormat)
#
# # 二进制化消息包
# # 包头(32bit,16bit,16bit) + 包体(Protocol数据)
# szFormat = "IHH%ds" % len(szMsg)
# buffer = struct.pack(szFormat, nTotalSize, 1, 0, szMsg)
# # print("test msg ", szMsg)
# # sock.send(buffer)
#
# time.sleep(1)
# sock.send(buffer)
#
# rsp = sock.recv(1000)
# print(rsp)
#
# time.sleep(3)
# szFormat = "IHH%ds" % len(szMsg)
# buffer = struct.pack(szFormat, nTotalSize, 1354, 0, szMsg)
# sock.send(buffer)
# # print("send done ", szMsg)
# rsp = sock.recv(3939)
# print(rsp)
# time.sleep(300)

    # print(szrsp)
    # nHeadSize = struct.calcsize("IHH")
    # print(struct.unpack("IHH", szrsp[:nHeadSize]))

    # 读取包体内容
    # szProtoBufData = szrsp[nHeadSize:]
    # po = recv_msg_pb2.recv_info()
    # po.ParseFromString(szProtoBufData)
    # print(po.session_id, po.request_type, po.request_data)
    # time.sleep(110.1)


