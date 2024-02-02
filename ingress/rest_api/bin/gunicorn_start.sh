#!/bin/bash
shopt -s expand_aliases
source ~/.bash_profile
NAME=almonitoring_rest_api
DIR=$(dirname "$0")
cd $DIR
WORKERS=3
WORKER_CLASS=uvicorn.workers.UvicornWorker
LOG_LEVEL=info
python -m gunicorn rest_api:app \
  --name $NAME \
  --chdir $(pwd)/../ \
  --workers $WORKERS \
  --worker-class $WORKER_CLASS \
  --bind 127.0.0.1:8000\
  --log-level=$LOG_LEVEL \
  --log-file=$(pwd)/../../../var/log/rest_api_gunicorn.log
