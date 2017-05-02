# -*- coding: utf-8 -*-
# @Author  : jh.feng
# -*- coding:utf-8 -*-
import socket
import struct, time

def PacketLoginBuff():
    import proto.login_pb2 as login_pb2
    req_login = login_pb2.login_req()
    global szMsg
    szMsg = "acc1"
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

def PacketQueryRoomScene():
    import proto.query_room_scene_pb2 as query_room_scene_pb2
    req_login = query_room_scene_pb2.query_room_scene_req()
    req_login.room_id = 0
    szAuthCode = req_login.SerializeToString()

    # 计算protobol消息体的字节数
    szFormat = "%ds" % len(szAuthCode)
    nTotalSize = struct.calcsize(szFormat)

    # 二进制化消息包
    # 包头(32bit,16bit,16bit) + 包体(Protocol数据)
    szFormat = "IHH%ds" % len(szAuthCode)
    return struct.pack(szFormat, nTotalSize, 10003, 0, szAuthCode)

def PacketEnterRoom(nRoomID):
    import proto.enter_room_pb2 as enter_room_pb2
    req = enter_room_pb2.enter_room_req()
    req.room_id = nRoomID
    szAuthCode = req.SerializeToString()

    # 计算protobol消息体的字节数
    szFormat = "%ds" % len(szAuthCode)
    nTotalSize = struct.calcsize(szFormat)

    # 二进制化消息包
    # 包头(32bit,16bit,16bit) + 包体(Protocol数据)
    szFormat = "IHH%ds" % len(szAuthCode)
    return struct.pack(szFormat, nTotalSize, 10011, 0, szAuthCode)


def PacketChangeScene(scene_name):
    import proto.change_scene_pb2 as change_scene_pb2
    req = change_scene_pb2.change_scene_req()
    req.scene_name = scene_name
    szAuthCode = req.SerializeToString()

    # 计算protobol消息体的字节数
    szFormat = "%ds" % len(szAuthCode)
    nTotalSize = struct.calcsize(szFormat)

    # 二进制化消息包
    # 包头(32bit,16bit,16bit) + 包体(Protocol数据)
    szFormat = "IHH%ds" % len(szAuthCode)
    return struct.pack(szFormat, nTotalSize, 10002, 0, szAuthCode)


def PacketEnterRoomBuff():
    szAuthCode = "aa"

    import proto.login_pb2 as login_pb2
    req_login = login_pb2.login_req()
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
    # sock = socket.create_connection(("192.168.74.130", 10242))
    sock = socket.create_connection(("127.0.0.1", 10242))
    sock.send(PacketLoginBuff())
    print(sock.recv(93939))

    # syn scene
    print(sock.recv(93939))

    sock.send(PacketQueryRoomScene())
    szRet = sock.recv(93939)
    print(szRet)

    szFormat = "IHH"
    nTotalBytes, cmd, flag = struct.unpack_from(szFormat, szRet)
    szRet = szRet[struct.calcsize(szFormat):]

    import proto.query_room_scene_pb2 as query_room_scene_pb2
    rsp = query_room_scene_pb2.query_room_scene_rsp()
    rsp.ParseFromString(szRet)

    print("room in scene ", rsp.scene_name, rsp.room_id)
    sock.send(PacketChangeScene(rsp.scene_name))
    sock.recv(399)

    sock.send(PacketEnterRoom(rsp.room_id))
    print("send enter room done.")

    while True:
        print(sock.recv(3948))
        time.sleep(1)


    time.sleep(9939)

    sock.close()
