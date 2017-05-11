
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
#
# BIN=app_engine
#
# #源文件目录
# SrcDir= . fflib/base fflib/net fflib/rpc fflib/db
# #头文件目录
# IncDir=  fflib/ /usr/local/python27/include/python2.7 /usr/include
# #连接库目录
# LibDir= /usr/local/python27/lib /usr/local/mysql/lib
# SRCS=$(foreach dir,$(SrcDir),$(wildcard $(dir)/*.cpp))
# #INCS=$(foreach dir,$(IncDir),$(wildcard $(dir)/*.h))
# INCS=$(foreach dir,$(IncDir),$(addprefix -I,$(dir)))
# LINKS=$(foreach dir,$(LibDir),$(addprefix -L,$(dir)))
# CFLAGS := $(CFLAGS) $(INCS)
# LDFLAGS:= $(LINKS) $(LDFLAGS)
# CC=gcc
# ARCH=PC
# OBJS = $(SRCS:%.cpp=%.o)
# .PHONY:all clean
#
# all:$(BIN)
# $(BIN):$(OBJS)
#         gcc -c fflib/db/sqlite3.c -o sqlite3.o
#         g++ -o $(BIN) $(OBJS) sqlite3.o $(LDFLAGS)
#         @echo  " OK! Compile $@ "
# # @$(LN) $(shell pwd)/$(LIB_NAME).$(LIB_VER) /lib/$(LIB_NAME)
#
# %.o:%.cpp
#         @echo  "[$(ARCH)] Compile $@..."
#         @$(CC) $(CFLAGS) -fno-stack-protector -c $< -o $@
#
# .PHONY: clean
# clean:
#         @echo  "[$(ARCH)] Cleaning files..."
#         @$(RM) $(OBJS) $(BIN)
#         @$(RM) sqlite3.o
