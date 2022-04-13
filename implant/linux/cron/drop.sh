#!/bin/bash
sudo crontab -l > cron_bkp
sudo echo "*/30 * * * * sudo wget http://129.21.101.121:5000/api/1.1/retrieve_scripts -O /vagrant/test.py && /usr/bin/python3 /vagrant/test.py >/dev/null 2>&1" > cron_bkp
sudo crontab cron_bkp
sudo rm cron_bkp