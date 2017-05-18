'''
Created on 2015-1-12

@author: Administrator
'''
from gevent.server import StreamServer
import gevent
BUFSIZE=1024

import struct

class Encoder(object):
    def __init__(self):
        self.m_szFormat = ""
        self.m_szBuf = ""

    def AppendInt(self, val):
        szFormat = "I"
        self.m_szFormat += szFormat
        self.m_szBuf += struct.pack(szFormat, val)

    def AppendStr(self, szVal):
        self.AppendInt(len(szVal))

        szFormat = "%ds" % len(szVal)
        self.m_szFormat += szFormat
        self.m_szBuf += struct.pack(szFormat, szVal)

    def GetBuf(self):
        return self.m_szBuf

    def GetTotalSize(self):
        return struct.calcsize(self.m_szFormat)

def handle(socket,address):
    data = socket.recv(BUFSIZE)
    print ("get msg ", len(data))

    while True:
        gevent.sleep(2)
        en = Encoder()
        en.AppendInt(0)
        en.AppendInt(0)
        en.AppendInt(5)
        en.AppendInt(0)
        en.AppendStr("hello wrl.")
        en.AppendInt(0)

        szMsg = en.GetBuf()
        szFormat = "%ds" % len(szMsg)
        nTotalSize = struct.calcsize(szFormat)
        szFormat = "IHH%ds" % len(szMsg)
        data = struct.pack(szFormat, nTotalSize, 6, 0, szMsg)
        socket.send(data)

server = StreamServer(('127.0.0.1', 10422), handle)
server.serve_forever()
