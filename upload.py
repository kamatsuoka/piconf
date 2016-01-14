#!/usr/bin/env python3

# Checks a directory for jpgs.  
# Starting with the oldest jpg:
# - compress to a smaller size
# - upload to Amazon Cloud Drive
# - delete original and resized version

import glob, os, subprocess, time

if __name__ == '__main__':
    source_dir = '/dev/shm/motion_capture'
    compressed_dir = '%s/compressed' % source_dir
    upload_dir = '/Pictures/picam'

    os.chdir(source_dir)

    while True:
        for f in glob.glob("*.jpg"):
            cmd = '/usr/bin/convert -strip -interlace Plane -gaussian-blur 0.05 -quality 85%% %s converted/%s' % (f, f)
            returncode = subprocess.call(cmd.split(' '), timeout=5)
            if returncode == 0:
                os.remove(f)
        time.sleep(1)
                
        
        
    
