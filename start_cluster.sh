#!/bin/bash

python3 main.py 1 > logs/partition1.log & \
python3 main.py 2 > logs/partition2.log& \
python3 main.py 3 > logs/partition3.log & \
python3 main.py 4 > logs/partition4.log & \
python3 main.py 5 > logs/partition5.log & \
python3 main.py 6 > logs/partition6.log & \
python3 main.py 7 > logs/partition7.log & \
python3 main.py 8 > logs/partition8.log & \
python3 main.py 9 > logs/partition9.log & \
python3 main.py 10 > logs/partition10.log & \
python3 main.py 11 > logs/partition11.log & \
python3 main.py 12 > logs/partition12.log