#!/bin/bash

set -e

services=(motion_capture compress upload)

case "$1" in
start|stop|restart|status)
  action = $1
  ;;
*)
  echo "Usage: $0 start|stop|restart|status" > /dev/stderr
  exit 1
  ;;
esac

services=(motion_capture compress upload)
for i in ${services[@]}; do
  sudo systemctl $action $i.service
done


