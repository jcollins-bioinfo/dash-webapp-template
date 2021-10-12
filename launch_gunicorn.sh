#!/bin/bash

# Gunicorn Launch script for Flask-based Dash app,
# ran concurrently, & in parallel.

TODAY=$(date "+%Y%m%d")
TIMESTAMP=$(date -Ins | tr -d "[[:punct:]]")

PORT=${1:-9001}
NUM_WORKERS=${2:-17}
THREADS=${3:-8}

GUNICORN_PROD_LOGS="./seqapp/app/prod/gunicorn/logs/${TODAY}"
mkdir -p $GUNICORN_PROD_LOGS

gunicorn \
  -b 0.0.0.0:$PORT \
  -w $NUM_WORKERS \
  --worker-class gthread \
  --threads $THREADS \
  --name "dash-webapp-template${TODAY}" \
  --max-requests 100 \
  --max-requests-jitter 10 \
  --access-logfile "${GUNICORN_PROD_LOGS}/${TODAY}.access.log" \
  app.wsgi:server


# --daemon \
# --reuse-port \
# --reload # intended for dev only \
# --worker-class gthread --threads $THREADS \
# --capture-output --log-file ${GUNICORN_PROD_LOGS}$(datetime)'.stderr.log.txt' --log-level DEBUG

## For SSL [HTTPS], if/when needed...
#--certfile cert.pem --keyfile key.pem &