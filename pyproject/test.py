import threading, time
from time import ctime,sleep

import test_create_room as test_create_room
import test_enter1 as test_enter1

import random
g_nOrder = random.randint(38474747, 2938388383)

def CreateRoom():
    test_create_room.StartUp()

def TestEnterRoom()\
        :
    global g_nOrder
    g_nOrder += 1
    test_enter1.StartUp(g_nOrder)

def StartGame():
    threads = []
    for i in xrange(0, 1):
        t1 = threading.Thread(target=CreateRoom)
        threads.append(t1)

    for t in threads:
        # t.setDaemon(True)
        t.start()

    # msg.conf_data.config_name = ""

        # t2 = threading.Thread(target=TestEnterRoom)
    # threads.append(t2)
    #
    # t21 = threading.Thread(target=fTestEnterRoom)
    # threads.append(t21)
    #
    # t22 = threading.Thread(target=TestEnterRoom)
    # threads.append(t22)
    # for t in threads:
    #     # t.setDaemon(True)
    #     time.sleep(0.1)
    #     t.start()

if __name__ == '__main__':
    for i in xrange(0, 1):
        print("start game ", i)
        print("\n" * 10)
        if i % 5 == 0:
            time.sleep(0.15)
        StartGame()
