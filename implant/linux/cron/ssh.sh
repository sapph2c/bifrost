#!/bin/bash
file="/etc/ssh/sshd_config"
setting="PubkeyAuthentication"
/usr/bin/sed -i '/^'"${setting}"'/d' ${file}
/usr/bin/echo "${setting} yes" >> ${file}
/usr/bin/systemctl reload sshd.service
