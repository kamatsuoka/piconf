#!/usr/bin/env python3

# Uploads jpgs to Amazon Cloud Drive, then deletes them

from datetime import date
from glob import glob
import os
import shutils
import subprocess
import sys
import time

from concurrent.futures import ThreadPoolExecutor

def upload(dir):
    """ uploads files in a directory tree, then deletes them.  
        dir is expected to be a year, with month and day directories under it."""
    try:
        cmd = 'acd_cli upload --remove-source-files --max-connections=4 %s Pictures/picam'
        return subprocess.call(cmd.split(' '), timeout=20)
    except:
        print("Unexpected error:", sys.exc_info()[0])

def         

if __name__ == '__main__':
    base_dir = sys.argv[1] if len(sys.argv) > 1 else '/dev/shm/motion_capture'
    upload_dir = '%s/upload' % base_dir
    for dir in [ base_dir, upload_dir ]:
        os.mkdirs(dir, exist_ok=True)

    while True:
        current_year = date.today().year
        for dir in glob('%s/*' % upload_dir):
            try:
                if os.path.isdir(dir):
                    dir_year = int(dir)
                    returncode = upload(dir)
                    if returncode == 0 and dir_year < current_year:
                        shutils.rmtree(dir)
            except:
                print('Unable to process directory %s under %s' % (dir, upload_dir))
        time.sleep(1)

    
