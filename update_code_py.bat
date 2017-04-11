@echo off
pscp -r -pw pascalx64 ./pylib reactor@192.168.74.130:/home/reactor/Documents/red_rabbit
pscp -r -pw pascalx64 ./pyproject reactor@192.168.74.130:/home/reactor/Documents/red_rabbit
pause