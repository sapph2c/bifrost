#!/bin/bash/
#
# Script that clears logs files on linux.
# First goes through files in /var/log/
# and then wipes each user's bash history.
#

for log_file in $(find /var/log -type f);
do
  > $log_file
done;

for home_dir in $(find /home/ -type d);
do
  > $home_dir/.bash_history
done;
