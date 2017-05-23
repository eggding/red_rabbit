'''
Created on 2015-1-12

@author: Administrator
'''
from gevent.server import StreamServer
from gevent import monkey; monkey.patch_all()
import gevent
import urllib2

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

# def f(url, sock):
#     print('GET: %s' % url)
#     resp = urllib2.urlopen(url)
#     data = resp.read()
#     SendMsg(sock, 8999, {"url": url})
#
# def handle(socket, address):
#     data = socket.recv(BUFSIZE)
#     print("get msg ", address, data)
#     gevent.joinall([
#         gevent.spawn(f, 'https://www.python.org/', socket),
#         gevent.spawn(f, 'https://www.yahoo.com/', socket),
#         gevent.spawn(f, 'https://github.com/', socket),
#     ])
#
# server = StreamServer(('127.0.0.1', 10422), handle)
# server.serve_forever()



import sys
import socket
import time
import gevent
from gevent import socket,monkey

monkey.patch_all()


def server(port):
    try:
        s = socket.socket()
        s.bind(('127.0.0.1', port))
        s.listen(500)
        while True:
            cli, addr = s.accept()
            gevent.spawn(handle_request, cli)
    except KeyboardInterrupt as e:
        s.close()


def handle_request(conn):
    try:
        c = 0
        while True:
            print("before start recv")
            data = conn.recv(1024)
            print("after start recv")
            if not data:
                #print("client has been closed...")
                #conn.shutdown(socket.SHUT_RD)
                conn.close()
            else:
                print("recv:", data)
                # conn.send(data)
                SendMsg(conn, 8999, str(c))
                c += 1
    except OSError as e:
        print("client has been closed")

    except Exception as ex:
        print(ex)
    finally:
        conn.close()

if __name__ == '__main__':
    server(10500)
