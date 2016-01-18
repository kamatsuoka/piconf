#!/usr/bin/env python3

# Checks a directory for jpgs.  
# Starting with the oldest jpg:
# - compress to a smaller size 
# - delete original


from concurrent.futures import ThreadPoolExecutor
from dateutil import parser
from glob import glob
import os
from os.path import basename, dirname
import re
import subprocess
import sys
import time
import traceback

datepattern = re.compile('\d{4}-\d{2}-\d{2}T')

def filedate(path):
    datestr = datepattern.search(path)
    date = parser.parse(datestr.group())
    return (date.year, date.month, date.day)

def compress(path):
    """ compresses a jpg to a smaller file in the 'compressed' dir,
        then moves the compressed file to the upload dir and deletes the original """
    try:
        convert_opts = '-strip -interlace Plane -gaussian-blur 0.05 -quality 85%'
        compressed_path = path.replace('/captured/', '/compressed/')
        cmd = 'convert %s %s %s' % (convert_opts, path, compressed_path)
        returncode = subprocess.call(cmd.split(' '), timeout=5)
        if returncode == 0:
            filename = basename(path)
            (y, m, d) = filedate(filename)
            upload_basedir = dirname(compressed_path).replace('/compressed', '/upload')
            upload_dir = '%s/%d/%02d/%02d' % (upload_basedir, y, m, d)
            os.makedirs(upload_dir, exist_ok=True)
            upload_path = '%s/%s' % (upload_dir, filename)
            print('renaming %s to %s' % (compressed_path, upload_path))
            os.rename(compressed_path, upload_path)
            os.remove(path)
    except:
        print("Unexpected error: %s " % traceback.format_exc())
        

if __name__ == '__main__':
    base_dir = sys.argv[1] if len(sys.argv) > 1 else '/dev/shm/motion_capture'
    captured_dir = '%s/captured' % base_dir
    compressed_dir = '%s/compressed' % base_dir
    upload_dir = '%s/upload' % base_dir
    for dir in [ base_dir, captured_dir, compressed_dir, upload_dir ]:
        os.makedirs(dir, exist_ok=True)

    try:
        while True:
            captured_files = glob('%s/*.jpg' % captured_dir)
            start_time = time.time()
            with ThreadPoolExecutor(max_workers=4) as executor:
                executor.map(compress, captured_files, timeout=60)
            if len(captured_files) > 0:
                print("Converted %s files in %s seconds" % (len(captured_files), time.time() - start_time))
            time.sleep(1)
    except KeyboardInterrupt:
        print('Interrupted')
    
