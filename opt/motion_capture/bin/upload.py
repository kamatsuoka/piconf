#!/usr/bin/env python3

# Uploads jpgs to Amazon Cloud Drive, then deletes them

from datetime import date
from glob import glob
import os
import shutil
import subprocess
import sys
import time
import traceback

from concurrent.futures import ThreadPoolExecutor

def upload(dir):
    """ uploads files in a directory tree, then deletes them.  
        dir is expected to be a year, with month and day directories under it."""
    try:
        acd_opts = '--force --remove-source-files --max-connections=8'
        cmd = 'acd_cli upload %s %s Pictures/picam' % (acd_opts, dir)
        # discarding stdout to avoid cluttering syslog with progress bar updates
        return subprocess.call(cmd.split(' '), stdout=subprocess.DEVNULL, timeout=60)
    except:
        print("Unexpected error: %s " % traceback.format_exc())

if __name__ == '__main__':
    base_dir = sys.argv[1] if len(sys.argv) > 1 else '/dev/shm/motion_capture'
    upload_dir = '%s/upload' % base_dir
    for dir in [ base_dir, upload_dir ]:
        os.makedirs(dir, exist_ok=True)

    while True:
        current_year = date.today().year
        for dir in glob('%s/*' % upload_dir):
            try:
                if os.path.isdir(dir):
                    dir_year = int(os.path.basename(dir))
                    returncode = upload(dir)
                    if returncode == 0 and dir_year < current_year:
                        shutil.rmtree(dir)
            except:
                print("Unexpected error: %s " % traceback.format_exc())
        time.sleep(1)

    
