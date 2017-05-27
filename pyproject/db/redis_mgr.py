# -*- coding: utf-8 -*-
# @Author  : jh.feng
import struct
class Encoder(object):
    def __init__(self):
        self.m_szFormat = ""
        self.m_szBuf = ""

    def AppendInt(self, val):
        szFormat = "I"
        self.m_szFormat += szFormat
        self.m_szBuf += struct.pack(szFormat, val)

    def AppendShortInt(self, val):
        szFormat = "H"
        self.m_szFormat += szFormat
        self.m_szBuf += struct.pack(szFormat, val)

    def AppendStr(self, szVal):
        szFormat = "I%ds" % len(szVal)
        self.m_szFormat += szFormat
        self.m_szBuf += struct.pack(szFormat, len(szVal), szVal)

    def GetBuf(self):
        return self.m_szBuf

    def GetTotalSize(self):
        return struct.calcsize(self.m_szFormat)


def SendMsg(sock, nCmd, dictMsg):
    en = Encoder()
    en.AppendShortInt(nCmd)

    import json
    en.AppendStr(json.dumps(dictMsg))
    szData = en.GetBuf()

    en = Encoder()
    en.AppendInt(999)
    en.AppendInt(999)
    en.AppendInt(5)
    en.AppendInt(0)
    en.AppendStr(szData)
    en.AppendInt(999)

    szMsg = en.GetBuf()
    szFormat = "%ds" % len(szMsg)
    nTotalSize = struct.calcsize(szFormat)
    szFormat = "IHH%ds" % len(szMsg)
    data = struct.pack(szFormat, nTotalSize, 6, 0, szMsg)
    sock.send(data)



from gevent.server import StreamServer

def handle(socket, address):
    socket.send("Hello from a telnet!\n")
    for i in range(5):
        socket.send(str(i) + '\n')

    import gevent
    def test(a, b):
        socket.send("test code.")

    loop = gevent.get_hub().loop
    t = loop.timer(0.0, 5)  # timer注册回调函数后马上调用回调函数，然后反复每隔5秒调用回调函数
    timer.start(test, 1, 2)
    loop.run()  # 运行反应器loop

        # socket.close()

server = StreamServer(('127.0.0.1', 5000), handle)
server.serve_forever()

