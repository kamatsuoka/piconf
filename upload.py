#!/usr/bin/env python3

# Checks a directory for jpgs.  
# Starting with the oldest jpg:
# - compress to a smaller size
# - upload to Amazon Cloud Drive
# - delete original and resized version

from glob import glob
import os, subprocess, time
from multiprocessing import Pool

def compress(f):
    """ compresses a jpg to a smaller file in the 'converted' dir and deletes the original """
    convert_opts = '-strip -interlace Plane -gaussian-blur 0.05 -quality 85%'
    cmd = '/usr/bin/convert %s %s converted/%s' % (convert_opts, f, f)
    returncode = subprocess.call(cmd.split(' '), timeout=5)
    if returncode == 0:
        os.remove(f)

if __name__ == '__main__':
    source_dir = '/dev/shm/motion_capture'
    compressed_subdir = '%s/compressed' % source_dir
    upload_dir = '/Pictures/picam'

    os.chdir(source_dir)

    with Pool(processes=4) as pool:
        while True:
            pool.map(compress, glob("*.jpg"), 1)
        time.sleep(1)
                
        
        
    
