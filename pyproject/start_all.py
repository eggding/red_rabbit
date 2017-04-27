import os, time
import conf as conf

szEngineBin = "./app_engine"
szSlave = "-slave "
szMaster = "-master 1"

szAddrMasterBroker = conf.dict_cfg["broker"]["listen_addr"]
szBrokerMaster = "-broker {0}".format(szAddrMasterBroker)

def KillAllProcess():
    os.system("ps -ef|grep app_engine |grep -v grep|cut -c 9-15|xargs kill -9")

def StartBrokerCluster():
    # os.system("./app_engine -master 1 -broker tcp://127.0.0.1:10241 &")
    # ./app_engine -slave 1 -broker tcp://127.0.0.1:11398 -master_broker tcp://127.0.0.1:10241 &
    # ./app_engine -slave 2 -broker tcp://127.0.0.1:11399 -master_broker tcp://127.0.0.1:10241 &
    # ./app_engine -slave 3 -broker tcp://127.0.0.1:11400 -master_broker tcp://127.0.0.1:10241 &

    # broker master
    os.system("{0} {1} {2} &".format(szEngineBin, szMaster, szBrokerMaster))
    time.sleep(0.1)

    # broker slave
    nMaxBrokerSlaveNum = 10
    for i in xrange(1, nMaxBrokerSlaveNum + 1):
        time.sleep(0.1)
        szKey = "broker_slave_{0}".format(i)
        if szKey not in conf.dict_cfg:
            break
        szSlaveAddr = conf.dict_cfg[szKey]["listen_addr"]
        os.system("{0} {1} {2} {3} {4} {5} &".format(szEngineBin, szSlave, i, szSlaveAddr, "-master_broker", szAddrMasterBroker))


def StartDbMgr():
    time.sleep(0.1)
    # ./app_engine -scene db_queue@ -broker tcp://127.0.0.1:10241 -python_path ./pyproject/db &
    szCodeDir = conf.dict_cfg["dbs"]["code_dir"]
    szCmd = "{0} -scene {1} {2} -python_path ./pyproject/{3} &".format(szEngineBin, "db_queue@", szBrokerMaster, szCodeDir)
    print("szCmd ", szCmd)
    os.system(szCmd)

    for i in xrange(0, conf.dict_cfg["dbs"]["queue_num"]):
        time.sleep(0.1)
        szCmd = "{0} -scene {1} {2} -python_path ./pyproject/{3} &".format(szEngineBin, "db_queue@{0}".format(i), szBrokerMaster, szCodeDir)
        print("szCmd ", szCmd)
        os.system(szCmd)

if __name__ == "__main__":
    KillAllProcess()
    StartBrokerCluster()
    StartDbMgr()
