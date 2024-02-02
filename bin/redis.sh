#!/bin/bash
if [ -z "%1" ]; then
  echo "Usage: ./script.sh [start|stop]"
  echo "start: start redis as daemon"
  echo "stop: stop redis"
elif [ "$1" == "start" ]; then
  cd "$(dirname "$0")"
  redis-server ../conf/redis.conf  --daemonize yes
elif [ "$1" == "stop" ]; then
  redis-cli -a 'redis' shutdown
else
  echo "Usage: ./script.sh [start|stop]"
  echo "start: start redis as daemon"
  echo "stop: stop redis"
fi
