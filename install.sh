#!/bin/bash

set -e

sudo rsync --recursive --update --verbose etc opt /
sudo systemctl daemon-reload
services=(motion_capture compress upload)
set -x
for i in ${services[@]}; do
  sudo systemctl enable $i.service
done
