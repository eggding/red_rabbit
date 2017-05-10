
import multiprocessing as multiprocessing
import time, random

def R(qret_, qjob_):
    import wsurl.http_mod as http_mod
    httpMgr = http_mod.GetUrlMgr()
    while True:
        szUrl = qjob.get()

        def _onGetHttpRet(httpRsp):
            qret_.put(httpRsp)

        httpMgr.Get(szUrl, _onGetHttpRet)
        httpMgr.DispatchRequest()

qret = multiprocessing.Queue()
qjob = multiprocessing.Queue()
p = multiprocessing.Process(target=R, args=(qret, qjob))
p.start()

p1 = multiprocessing.Process(target=R, args=(qret, qjob))
p1.start()
#
# p2 = multiprocessing.Process(target=R, args=(qret, qjob))
# p2.start()

c = 0
def ProdJob():
    # print("ProdJob")
    t = random.randint(1, 8) / 10
    tick_mgr.RegisterOnceTick(t * 1000, ProdJob)
    szUrl = "https://g51-udataresys.nie.netease.com:8443/Recommender/FriendshipService?request=friendship_data&gameId=g51&token=tHAf25XUgM8Amfj&orderId=1852038034&server=1003&roleId=583a3c72353e9d0b47b92599&friends="
    # GetUrlMgr().Get(szUrl, callback=cb)
    qjob.put(szUrl)

def GetRet():
    tick_mgr.RegisterOnceTick(10, GetRet)
    if qret.empty() is True:
        return
    job = qret.get()
    global c
    c += 1
    print("main get job ret ", c, qret.qsize())

ProdJob()
GetRet()