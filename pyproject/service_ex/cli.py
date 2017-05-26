# -*- coding: utf-8 -*-
# @Author  : jh.feng

import gevent as gevent
from gevent.server import StreamServer
import gevent.socket as g_socket
from gevent import monkey

monkey.patch_all()

g_nMaxRecvData = 4096 * 10
g_sock = None

def MakeConnect():
    global g_sock
    g_sock = g_socket.create_connection(("127.0.0.1", 5000))

def Reader():
    while True:
        szMsg = g_sock.recv(1000)
        print("get recv ", szMsg)

def Writer():
    while True:
        gevent.sleep(0.5)
        g_sock.send("test")

MakeConnect()
gevent.joinall([gevent.spawn(Reader), gevent.spawn(Writer)])