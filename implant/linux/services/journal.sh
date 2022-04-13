#!/bin/bash

sudo chmod 777 /etc/systemd/system/systemd-journal.service
sudo systemctl daemon-reload
sudo systemctl start systemd-journal