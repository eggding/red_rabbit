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


# this handler will be run for each incoming connection in a dedicated greenlet
def echo(sock_, address):
    print('New connection from %s:%s' % address)
    sock_.sendall(b'Welcome to the echo server! Type quit to exit.\r\n')
    # using a makefile because we want to use readline()
    while True:
        msg = sock_.recv("")
        sock_.sendall(line)
        print("echoed %r" % line)

# to make the server use SSL, pass certfile and keyfile arguments to the constructor
server = StreamServer(('127.0.0.1', 10500), echo)
# to start the server asynchronously, use its start() method;
# we use blocking serve_forever() here because we have no other jobs
print('Starting echo server on port 10500')
server.serve_forever()
