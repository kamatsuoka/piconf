#!/usr/bin/env python3

import picamera

with picamera.PiCamera() as camera:
    camera.resolution = (1024, 768)
    camera.vflip = True
    camera.framerate = 15
    camera.start_preview()
    camera.start_recording('foo.h264', resize=(256, 192))
    camera.wait_recording(2)
    print('encoding = %s' % camera._get_still_encoding())
    print(camera._get_resolution())
#    camera.capture('foo.data', 'yuv')
    camera.capture('foo-video.jpg', use_video_port=True)
    camera.stop_recording()
