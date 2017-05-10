# -*- coding: utf-8 -*-
# @Author  : jh.feng

import struct

class BinEncoder(object):
    def __init__(self):
        self.m_szBuf = ""
        self.m_nTotalSize = 0

    def AppendStr(self, szMsg):
        szFormat = "I"
        self.m_szBuf += struct.pack(szFormat, len(szMsg))
        self.m_nTotalSize += struct.calcsize(szFormat)

        szFormat = "%ds" % len(szMsg)
        self.m_szBuf += struct.pack(szFormat, szMsg)
        self.m_nTotalSize += struct.calcsize(szFormat)

    def AppendInt(self, nVal):
        szFormat = "i"
        self.m_szBuf += struct.pack(szFormat, nVal)
        self.m_nTotalSize += struct.calcsize(szFormat)

    def Encode(self, cmd):
        szFormat = "IHH%ds" % len(self.m_szBuf)
        return struct.pack(szFormat, self.m_nTotalSize, cmd, 0, self.m_szBuf)

class BinDecoder(object):
    def __init__(self, buf):
        self.m_szBuf = buf

    def GetBytes(self, nbytes):
        assert len(self.m_szBuf) >= nbytes
        data = self.m_szBuf[:nbytes]
        self.m_szBuf = self.m_szBuf[nbytes + 1:]
        return data

    def GetStr(self):
        nStrLen = self.GetInt()
        szContent = self.GetBytes(nStrLen)
        return szContent

    def GetInt(self):
        szFormat = "i"
        nSize = struct.calcsize(szFormat)
        return int(self.GetBytes(nSize))


# -*- coding:utf-8 -*-

import sys
import socket, struct
import time
import gevent
from gevent import socket

# service_name << msg_names << binder_broker_node_id
# static void send(socket_ptr_t socket_ptr_, uint16_t cmd_, codec_i& msg_)
# {
#     if (socket_ptr_)
#     {
#         string body = msg_.encode_data();
#         message_head_t h(cmd_);
#         h.size = body.size();
#         string dest((const char*)&h, sizeof(h));
#         dest += body;
#
#         socket_ptr_->async_send(dest);
#     }
# }

BROKER_CLIENT_REGISTER = 3

# service_name << msg_names << binder_broker_node_id
class BinEncoder(object):
    def __init__(self):
        self.m_szBuf = ""
        self.m_nTotalSize = 0

    def AppendStr(self, szMsg):
        szFormat = "I"
        self.m_szBuf += struct.pack(szFormat, len(szMsg))
        self.m_nTotalSize += struct.calcsize(szFormat)

        szFormat = "%ds" % len(szMsg)
        self.m_szBuf += struct.pack(szFormat, szMsg)
        self.m_nTotalSize += struct.calcsize(szFormat)

    def AppendInt(self, nVal):
        szFormat = "i"
        self.m_szBuf += struct.pack(szFormat, nVal)
        self.m_nTotalSize += struct.calcsize(szFormat)

    def Encode(self, cmd):
        print("ntotal size ", self.m_nTotalSize)
        szFormat = "IHH%ds" % len(self.m_szBuf)
        return struct.pack(szFormat, self.m_nTotalSize, cmd, 0, self.m_szBuf)

def server(port):
    encoder = BinEncoder()
    s = socket.create_connection(("127.0.0.1", 10241))
    print(s.getpeername())
    szServiceName = "gevent_test"
    listService = ["v1", "v2"]
    encoder.AppendStr(szServiceName)
    encoder.AppendInt(len(listService))
    for szOneService in listService:
        encoder.AppendStr(szOneService)
    encoder.AppendInt(0)
    binMsg = encoder.Encode(BROKER_CLIENT_REGISTER)
    s.send(binMsg)
    szMsg = s.recv(3883)

if __name__ == '__main__':
    server(7777)