#!/bin/bash
cd "$(dirname "$0")"

while getopts h:s:j: flag
do
  case "${flag}" in
    h) hostname=${OPTARG};;
    s) sleepTime=${OPTARG};;
    j) jitter=${OPTARG};;
  esac
done

go build -ldflags="-X 'main.IP=$hostname' -X 'main.SleepTime=$sleepTime'"
