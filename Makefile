#交叉编译器路径
CROSS=
CP=/bin/cp
RM=-/bin/rm -rf
LN=/bin/ln -s 
CFLAGS=-g  -Wall
LDFLAGS= -lpthread  -ldl -lpython2.7 -lmysqlclient
#链接库名
LIB_NAME=
#链接库版本
LIB_VER=1.0.0
#平台
ARCH=
# 二进制目标
BIN=app_engine

#源文件目录
SrcDir= . fflib/base fflib/net fflib/rpc fflib/db
#头文件目录
IncDir=  fflib/  /usr/include/python2.7/ /usr/include/python2.6/
#连接库目录
LibDir= /usr/local/lib /usr/lib/mysql
SRCS=$(foreach dir,$(SrcDir),$(wildcard $(dir)/*.cpp))
#INCS=$(foreach dir,$(IncDir),$(wildcard $(dir)/*.h))
INCS=$(foreach dir,$(IncDir),$(addprefix -I,$(dir)))
LINKS=$(foreach dir,$(LibDir),$(addprefix -L,$(dir)))
CFLAGS := $(CFLAGS) $(INCS)
LDFLAGS:= $(LINKS) $(LDFLAGS) 
CC=gcc
ARCH=PC
OBJS = $(SRCS:%.cpp=%.o)
.PHONY:all clean

all:$(BIN)
$(BIN):$(OBJS)
	gcc -c fflib/db/sqlite3.c -o sqlite3.o
	g++ -o $(BIN) $(OBJS) sqlite3.o $(LDFLAGS)  
	@echo  " OK! Compile $@ "
# @$(LN) $(shell pwd)/$(LIB_NAME).$(LIB_VER) /lib/$(LIB_NAME)

%.o:%.cpp
	@echo  "[$(ARCH)] Compile $@..."
	@$(CC) $(CFLAGS) -fno-stack-protector -c $< -o $@

.PHONY: clean
clean:
	@echo  "[$(ARCH)] Cleaning files..."
	@$(RM) $(OBJS) $(BIN) 
	@$(RM) sqlite3.o
