#!/bin/bash

#rm ./datas/*

wget -O proxies.txt https://api.proxyscrape.com/?request=getproxies&proxytype=http&timeout=2000

python3.7 main.py 2>> error
