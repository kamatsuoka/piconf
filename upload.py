#!/usr/bin/env python3

# Checks a directory for jpgs.  
# Starting with the oldest jpg:
# - compress to a smaller size
# - upload to Amazon Cloud Drive
# - delete original and resized version

from glob import glob
import os, subprocess, time
import sys
import time

# continually looks for files in captured_dir and converts them to a smaller size.

def compress(filename):
    """ compresses a jpg to a smaller file in the 'converted' dir and deletes the original """
    convert_opts = '-strip -interlace Plane -gaussian-blur 0.05 -quality 85%'
    converted_filename = filename.replace('/captured/', '/converted/')
    cmd = 'convert %s %s %s' % (convert_opts, filename, converted_filename)
    returncode = subprocess.call(cmd.split(' '), timeout=5)
    if returncode == 0:
        os.remove(filename)

if __name__ == '__main__':
    base_dir = sys.argv[1] if len(sys.argv) > 1 else '/dev/shm/motion_capture'
    captured_dir = '%s/captured' % base_dir
    converted_dir = '%s/converted' % base_dir
    upload_dir = '%s/upload' % base_dir
    for dir in [ base_dir, captured_dir, converted_dir, upload_dir ]:
        if not os.path.isdir(dir):
            os.mkdir(dir)

    try:
        while True:
            for filename in glob('%s/*.jpg' % captured_dir):
                compress(filename)
            time.sleep(1)
    except KeyboardInterrupt:
        print('Interrupted')
    
