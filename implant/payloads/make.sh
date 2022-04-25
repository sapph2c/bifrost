#!/bin/bash
cd /home/lights0ut/RedTeam/Bifrost/implant/payloads

while getopts h:s:j: flag
do
  case "${flag}" in
    h) hostname=${OPTARG};;
    s) sleepTime=${OPTARG};;
    j) jitter=${OPTARG};;
  esac
done

/usr/bin/go build -ldflags="-X 'main.IP=$hostname' -X 'main.SleepTime=$sleepTime'"
