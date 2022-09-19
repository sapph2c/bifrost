#!/bin/bash

while getopts h:s:j: flag
do
  case "${flag}" in
    h) hostname=${OPTARG};;
    s) sleepTime=${OPTARG};;
    j) jitter=${OPTARG};;
  esac
done

cd /Bifrost/src/agent
/usr/local/go/bin/go build -buildvcs=false -ldflags="-X 'main.IP=$hostname' -X 'main.SleepTime=$sleepTime'"
