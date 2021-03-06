# -*- coding: utf-8 -*-
# @Author  : jh.feng
# -*- coding:utf-8 -*-
import socket
import struct, time



szCode = """
from greenlet import greenlet
def test1():
    print(12)
    gr2.switch()
    print(34)
    gr2.switch()
def test2():
    print(56)
    gr1.switch()
    print(78)
gr1 = greenlet(test1)
gr2 = greenlet(test2)
gr1.switch()
"""


def PackSendGmCode():
    szScene = "all_gas"
    szToken = "585231e1353e9d56e284b8a9"
    import proto.login_pb2 as login_pb2
    req_login = login_pb2.login_req()
    req_login.type = 3
    req_login.auth_info = "{0}#{1}#{2}".format(szToken, szScene, szCode)
    szMsg = "航空自卫队" #  req_login.SerializeToString()
    # 计算protobol消息体的字节数
    szFormat = "%ds" % len(szMsg)
    nTotalSize = struct.calcsize(szFormat)

    # 二进制化消息包
    # 包头(32bit,16bit,16bit) + 包体(Protocol数据)
    szFormat = "IHH%ds" % len(szMsg)
    return struct.pack(szFormat, nTotalSize, 10001, 0, szMsg)

while True:
    sock = socket.create_connection(("112.74.124.100", 9501))
    # sock = socket.create_connection(("127.0.0.1", 10242))
    sock.send(PackSendGmCode())
    print(sock.recv(93939))
    time.sleep(39)
    # sock.send(PacketLoginBuff())
    # print(sock.recv(93939))
    #
    # # syn scene
    # print(sock.recv(93939))
    #
    # sock.send(PacketQueryRoomScene())
    # szRet = sock.recv(93939)
    # print(szRet)
    #
    # szFormat = "IHH"
    # nTotalBytes, cmd, flag = struct.unpack_from(szFormat, szRet)
    # szRet = szRet[struct.calcsize(szFormat):]
    #
    # import proto.query_room_scene_pb2 as query_room_scene_pb2
    # rsp = query_room_scene_pb2.query_room_scene_rsp()
    # rsp.ParseFromString(szRet)
    #
    # print("room in scene ", rsp.scene_name, rsp.room_id)
    # sock.send(PacketChangeScene(rsp.scene_name))
    # sock.recv(399)
    #
    # sock.send(PacketEnterRoom(rsp.room_id))
    # print("send enter room done.")
    #
    # time.sleep(1)
    # sock.send(PacketExeCode())
    # print("send exe code done.")
    #
    # while True:
    #     print(sock.recv(3948))
    #     time.sleep(1)
    #
    #
    # time.sleep(9939)
    #
    # sock.close()
