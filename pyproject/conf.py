# -*- coding:utf-8 -*-
import os

def GetLocalIP():
    # return "127.0.0.1"
    out = os.popen("ifconfig | grep 'inet addr:' | grep -v '127.0.0.1' | cut -d: -f2 | awk '{print $1}' | head -1").read()
    return out[:-1]

def GetPwd():
    dictTmp = {
        "112.74.124.100": "2VP8lYkg",
    }
    return dictTmp.get(GetLocalIP(), "pascalx64")

dict_cfg = {
    "server_id": 1,
    "debug_env": True,

    "broker": {
        "listen_addr": "tcp://127.0.0.1:10241"
    },
    "broker_slave_1": {
        "listen_addr": "tcp://127.0.0.1:10341"
    },
    "broker_slave_2": {
        "listen_addr": "tcp://127.0.0.1:10342"
    },
    "dbs": {
        "queue_num": 3,
        "host": "localhost:3306",
        "user": "root",
        "db": "red_rabbit",
        "pwd": "{0}".format(GetPwd()),
    },
    "gate": {
        "gate@master": "tcp://{0}:10245".format(GetLocalIP()),
        "gate@0": "tcp://{0}:10242".format(GetLocalIP()),
        "gate@1": "tcp://{0}:10243".format(GetLocalIP()),
    },
    "gas": {
        "num": 3,
        "robot_num": 10,
    },
    "gm_service": {

    }
}