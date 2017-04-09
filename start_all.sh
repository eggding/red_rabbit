ps -ef|grep app_engine |grep -v grep|cut -c 9-15|xargs kill -9

./app_engine -main-broker 1 -broker tcp://127.0.0.1:10241 &
sleep 0.1
./app_engine -gate gate@0 -gate_listen tcp://127.0.0.1:10242 -broker tcp:://127.0.0.1:10241 &
sleep 0.1
./app_engine -scene scene@0 -broker tcp://127.0.0.1:10241 -python_path ./pyproject/login/ &
sleep 0.1
./app_engine -scene scene@1 -broker tcp://127.0.0.1:10241 -python_path ./pyproject/room_service &
