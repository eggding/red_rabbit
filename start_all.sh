ps -ef|grep app_redrabbit |grep -v grep|cut -c 9-15|xargs kill -9

./app_redrabbit -main-broker 1 -broker tcp://127.0.0.1:10241 &
sleep 0.1
./app_redrabbit -gate gate@0 -gate_listen tcp://127.0.0.1:10242 -broker tcp:://127.0.0.1:10241 &
sleep 0.1
./app_redrabbit -scene scene@0 -broker tcp://127.0.0.1:10241 -python_path ./pyproject/login/ &
sleep 0.1
./app_redrabbit -scene scene@1 -broker tcp://127.0.0.1:10241 -python_path ./pyproject/room_service &
