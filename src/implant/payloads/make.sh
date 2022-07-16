#!/bin/bash

while getopts h:s:j: flag
do
  case "${flag}" in
    h) hostname=${OPTARG};;
    s) sleepTime=${OPTARG};;
    j) jitter=${OPTARG};;
  esac
done

cd /app/implant/payloads/
/usr/local/go/bin/go build -buildvcs=false -ldflags="-X 'main.IP=$hostname' -X 'main.SleepTime=$sleepTime'"
