# -*- coding: utf-8 -*-
# @Author  : jh.feng
# -*- coding:utf-8 -*-
import socket
import struct, time

gIndex = 0

def PacketLoginBuff():
    import proto.login_pb2 as login_pb2
    req_login = login_pb2.login_req()
    global szMsg
    import random
    global gIndex
    szMsg = "acc0" + str(gIndex)
    gIndex += 1
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

def PackSetConf():
    import proto.gm_config_pb2 as gm_config_pb2
    req = gm_config_pb2.opt_config_req()
    req.opt_type = gm_config_pb2.gm_config_opt.Value("apply")
    req.conf_data.config_name = "test_config"
    req.conf_data.pos_1_card = "101,102,103,104,105,106,107,108,109,501,402,403,404"
    req.conf_data.pos_2_card = "201,202,203,204,205,206,207,208,209,502,503,504,404,505"
    req.conf_data.pos_3_card = "301,302,303,304,305,306,307,308,309,405,402,403,404"
    req.conf_data.pos_4_card = "401,402,403,404,405,406,407,308,309,405,402,403,506"

    import gas.gas_mj.check_hu as check_hu
    import copy
    g_listAllMj = copy.copy(check_hu.g_mjsArr)
    for i in xrange(1, 5):
        szData = getattr(req.conf_data, "pos_{0}_card".format(i))
        assert szData is not None

        listTmp = map(int, szData.split(","))
        for nCard in listTmp:
            assert nCard in g_listAllMj, nCard
            g_listAllMj.remove(nCard)

    szRet = ""
    for nCard in g_listAllMj:
        if len(szRet) != 0:
            szRet += ","
        szRet += str(nCard)
    req.conf_data.card_order = szRet

    szAuthCode = req.SerializeToString()

    # 计算protobol消息体的字节数
    szFormat = "%ds" % len(szAuthCode)
    nTotalSize = struct.calcsize(szFormat)

    # 二进制化消息包
    # 包头(32bit,16bit,16bit) + 包体(Protocol数据)
    szFormat = "IHH%ds" % len(szAuthCode)
    return struct.pack(szFormat, nTotalSize, 10051, 0, szAuthCode)


def PacketEnterRoom(nRoomID):
    import proto.gm_config_pb2 as gm_config_pb2
    req = gm_config_pb2.syn_all_gm_config_req()
    szAuthCode = req.SerializeToString()

    # 计算protobol消息体的字节数
    szFormat = "%ds" % len(szAuthCode)
    nTotalSize = struct.calcsize(szFormat)

    # 二进制化消息包
    # 包头(32bit,16bit,16bit) + 包体(Protocol数据)
    szFormat = "IHH%ds" % len(szAuthCode)
    return struct.pack(szFormat, nTotalSize, 10050, 0, szAuthCode)

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

def PacketGetGate():
    szAuthCode = "aa"

    import proto.login_pb2 as login_pb2
    req = login_pb2.login_req()
    req.type = login_pb2.login_type.Value("get_gate_info")
    req.auth_info = szAuthCode
    szAuthCode = req.SerializeToString()

    # 计算protobol消息体的字节数
    szFormat = "%ds" % len(szAuthCode)
    nTotalSize = struct.calcsize(szFormat)

    # 二进制化消息包
    # 包头(32bit,16bit,16bit) + 包体(Protocol数据)
    szFormat = "IHH%ds" % len(szAuthCode)
    return struct.pack(szFormat, nTotalSize, 10001, 0, szAuthCode)


def StartUp(nId=None):
    if nId is None:
        import random
        nId = random.randint(1, 984784)
    global gIndex
    gIndex = nId
    while True:
        # sock = socket.create_connection(("112.74.124.100", 10242))
        # sock = socket.create_connection(("192.168.74.130", 10242))
        sock = socket.create_connection(("127.0.0.1", 10242))
        # sock.send(PackSetConf())
        # print(sock.recv(4444))
        # sock.send("333")
        # print(sock.recv(4444))
        sock.send(PacketLoginBuff())
        print(sock.recv(93939))

        # syn scene
        print(sock.recv(93939))

        # sock.send(PacketQueryRoomScene())
        # szRet = sock.recv(93939)
        # print(szRet)

        # szFormat = "IHH"
        # nTotalBytes, cmd, flag = struct.unpack_from(szFormat, szRet)
        # szRet = szRet[struct.calcsize(szFormat):]

        # import proto.query_room_scene_pb2 as query_room_scene_pb2
        # rsp = query_room_scene_pb2.query_room_scene_rsp()
        # rsp.ParseFromString(szRet)

        # print("room in scene ", rsp.scene_name, rsp.room_id)
        # sock.send(PacketChangeScene(rsp.scene_name))
        # sock.recv(399)

        # sock.send(PacketEnterRoom(0))
        # print("11 .")
        # print(sock.recv(3884))
        #
        sock.send(PackSetConf())
        print(sock.recv(3884))

        # while True:
        #     # print(sock.recv(3948))
        #     tmp = sock.recv(39484)
        #     time.sleep(1)


        time.sleep(9939)

        sock.close()

if __name__ == "__main__":
    import random
    StartUp(random.randint(1, 984784))
