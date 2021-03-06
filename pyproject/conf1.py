# -*- coding:utf-8 -*-

dict_cfg = {
    "broker": {
        "listen_addr": "tcp://192.168.74.130:10241"
    },
    "broker_slave_1": {
        "listen_addr": "tcp://192.168.74.130:10341"
    },
    "broker_slave_2": {
        "listen_addr": "tcp://192.168.74.130:10342"
    },
    "dbs": {
        "queue_num": 2,
        "host": "localhost:3306",
        "user": "root",
        "db": "red_rabbit",
        "pwd": "pascalx64",
    },
    "gate": {
        "gate@master": "tcp://192.168.74.131:10245",
        "gate@0": "tcp://192.168.74.131:10242",
        "gate@1": "tcp://192.168.74.131:10243",
    },
    # "gate": {
    #     "gate@master": "tcp://127.0.0.1:10245",
    #     "gate@0": "tcp://127.0.0.1:10242",
    #     "gate@1": "tcp://127.0.0.1:10243",
    # },
    "gas": {
        "num": 3
    }
}