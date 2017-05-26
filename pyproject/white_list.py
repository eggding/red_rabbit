# -*- coding: utf-8 -*-
# @Author  : jh.feng

# import gevent as gevent
# from gevent.server import StreamServer
#
# g_nMaxRecvData = 4096 * 10
#
# def producer():
#     gevent.with_timeout(1, producer)
#     print("test producer..")
#
# def handle(socket, address):
#     print("connect come ", address)
#     while True:
#         szMsg = socket.recv(g_nMaxRecvData)
#         print("recv from ", address, szMsg)
#
# producer()
#
# server = StreamServer(('127.0.0.1', 5000), handle)
# server.serve_forever()
