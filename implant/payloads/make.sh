#!/bin/bash

while getopts h:s:j: flag
do
  case "${flag}" in
    h) hostname=${OPTARG};;
    s) sleepTime=${OPTARG};;
    j) jitter=${OPTARG};;
  esac
done

HOME=/home/lights0ut/
cd /home/lights0ut/RedTeam/Bifrost/implant/payloads
PATH=$PATH:/usr/local/go/bin GOPATH=/home/lights0ut/RedTeam/Bifrost/implant /usr/bin/go build -buildvcs=false -ldflags="-X 'main.IP=$hostname' -X 'main.SleepTime=$sleepTime'"
