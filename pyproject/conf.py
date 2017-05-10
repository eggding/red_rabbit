# -*- coding:utf-8 -*-

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
        "pwd": "pascalx64",
    },
    "gate": {
        "gate@master": "tcp://192.168.74.130:10245",
        "gate@0": "tcp://192.168.74.130:10242",
        "gate@1": "tcp://192.168.74.130:10243",
    },
    # "gate": {
    #     "gate@master": "tcp://127.0.0.1:10245",
    #     "gate@0": "tcp://127.0.0.1:10242",
    #     "gate@1": "tcp://127.0.0.1:10243",
    # },
    "gas": {
        "num": 3
    },
    "gm_service": {

    }
}