#!/bin/bash
pid=`ps ax | grep gunicorn | awk '{split($0,a," "); print a[1]}' | head -n 1`
if [ -z "$pid" ]; then
  echo "no gunicorn deamon running..."
else
  kill $pid
  echo "killed gunicorn deamon."
fi
