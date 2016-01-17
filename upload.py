#!/usr/bin/env python3

# Checks a directory for jpgs.  
# Starting with the oldest jpg:
# - upload to Amazon Cloud Drive
# - delete jpg

from glob import glob
import os, subprocess, time
import sys
import time

# TODO: logging

from concurrent.futures import ThreadPoolExecutor

def upload(filename):
    """ uploads a jpg, then deletes it """
    try:
        cmd = 'acd_cli upload %s Pictures/picam' % filename
        returncode = subprocess.call(cmd.split(' '), timeout=20)
        if returncode == 0:
            print('removing %s' % filename)
            os.remove(filename)
    except:
        print("Unexpected error:", sys.exc_info()[0])

if __name__ == '__main__':
    base_dir = sys.argv[1] if len(sys.argv) > 1 else '/dev/shm/motion_capture'
    upload_dir = '%s/upload' % base_dir
    for dir in [ base_dir, upload_dir ]:
        if not os.path.isdir(dir):
            os.mkdir(dir)

    while True:
        with ThreadPoolExecutor(max_workers=4) as executor:
            executor.map(upload, glob('%s/*.jpg' % upload_dir), timeout=60)
        time.sleep(1)

    
