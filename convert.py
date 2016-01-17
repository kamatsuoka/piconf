#!/usr/bin/env python3

# Checks a directory for jpgs.  
# Starting with the oldest jpg:
# - compress to a smaller size 
# - delete original

from glob import glob
import os, subprocess, time
import sys
import time

def compress(filename):
    """ compresses a jpg to a smaller file in the 'compressed' dir,
        then moves the compressed file to the upload dir and deletes the original """
    convert_opts = '-strip -interlace Plane -gaussian-blur 0.05 -quality 85%'
    compressed_filename = filename.replace('/captured/', '/compressed/')
    cmd = 'convert %s %s %s' % (convert_opts, filename, compressed_filename)
    returncode = subprocess.call(cmd.split(' '), timeout=5)
    if returncode == 0:
        upload_filename = compressed_filename.replace('/compressed/', '/upload/')
        print('renaming %s to %s' % (compressed_filename, upload_filename))
        os.rename(compressed_filename, upload_filename)
        os.remove(filename)

if __name__ == '__main__':
    base_dir = sys.argv[1] if len(sys.argv) > 1 else '/dev/shm/motion_capture'
    captured_dir = '%s/captured' % base_dir
    compressed_dir = '%s/compressed' % base_dir
    upload_dir = '%s/upload' % base_dir
    for dir in [ base_dir, captured_dir, compressed_dir, upload_dir ]:
        if not os.path.isdir(dir):
            os.mkdir(dir)

    try:
        while True:
            for filename in glob('%s/*.jpg' % captured_dir):
                compress(filename)
            time.sleep(1)
    except KeyboardInterrupt:
        print('Interrupted')
    
