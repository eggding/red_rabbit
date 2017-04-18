
rm -rf /usr/lib/mysql/plugin/udf_json.so 
gcc -fPIC -Wall -I/usr/include/mysql -I. -shared cJSON.c udf_redis.c -o udf_json.so
cp udf_json.so /usr/lib/mysql/plugin/
mysql -u root -p < json.sql