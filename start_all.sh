ps -ef|grep app_engine |grep -v grep|cut -c 9-15|xargs kill -9

# broker master
./app_engine -master 1 -broker tcp://127.0.0.1:10241 &
sleep 0.1

# broker slave
./app_engine -slave 1 -broker tcp://127.0.0.1:10398 -master_broker tcp://127.0.0.1:10241 &
./app_engine -slave 2 -broker tcp://127.0.0.1:10399 -master_broker tcp://127.0.0.1:10241 &

# dbs 任务持久化任务队列
./app_engine -scene db_queue@ -broker tcp://127.0.0.1:10241 -python_path ./pyproject/db &
./app_engine -scene db_queue@0 -broker tcp://127.0.0.1:10241 -python_path ./pyproject/db &
./app_engine -scene db_queue@1 -broker tcp://127.0.0.1:10241 -python_path ./pyproject/db &
./app_engine -scene db_queue@2 -broker tcp://127.0.0.1:10241 -python_path ./pyproject/db &
./app_engine -scene db_queue@3 -broker tcp://127.0.0.1:10241 -python_path ./pyproject/db &
sleep 0.1

./app_engine -scene scene@0 -broker tcp://127.0.0.1:10241 -python_path ./pyproject/login/ &
sleep 0.1

./app_engine -scene room_service -broker tcp://127.0.0.1:10241 -python_path ./pyproject/room_service &
sleep 0.1

# ./app_engine -name gate@0 -gate gate@0 -gate_listen tcp://127.0.0.1:10242 -broker tcp:://127.0.0.1:10241 &
./app_engine -gate gate@0 -gate_listen tcp://192.168.74.130:10242 -broker tcp:://127.0.0.1:10241 &
