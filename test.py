# -*- coding:utf-8 -*-
import socket

sock = socket.create_connection(("127.0.0.1", 10242))
# sock = socket.create_connection(("112.74.124.100", 10341))
# protocol 消息
import pyproject.proto.recv_msg_pb2 as recv_msg_pb2
po = recv_msg_pb2.recv_info()
po.request_type = 4001
po.session_id = "3283489584848xx"
po.request_data = "pascal"
szMsg = po.SerializeToString()

# 计算protobol消息体的字节数
import struct
szFormat = "%ds" % len(szMsg)
nTotalSize = struct.calcsize(szFormat)

# 二进制化消息包
# 包头(32bit,16bit,16bit) + 包体(Protocol数据)
szFormat = "IHH%ds" % len(szMsg)
buffer = struct.pack(szFormat, nTotalSize, 1001, 0, szMsg)
print("test msg ", szMsg)

while True:
    import time
    sock.send(buffer)
    szrsp = sock.recv(10000)# print 'Original values:', values

    # print(szrsp)
    nHeadSize = struct.calcsize("IHH")
    print(struct.unpack("IHH", szrsp[:nHeadSize]))

    # 读取包体内容
    szProtoBufData = szrsp[nHeadSize:]
    po = recv_msg_pb2.recv_info()
    po.ParseFromString(szProtoBufData)
    print(po.session_id, po.request_type, po.request_data)
    time.sleep(110.1)
