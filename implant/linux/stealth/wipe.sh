#!/bin/bash/
#
# Script that clears logs files on linux.
# First goes through files in /var/log/
# and then wipes each user's bash history.
#

for log_file in $(find /var/log -type f);
do
  echo 0> $log_file
done;

for home_dir in $(find /home/ -type d);
do
  echo 0> $home_dir/.bash_history
done;
