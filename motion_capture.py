#!/usr/bin/env python3 

import datetime
import os
import time

import numpy as np
import picamera
import picamera.array

class DetectMotion(picamera.array.PiMotionAnalysis):

    def __init__(self, camera, motion_threshold, min_blocks, min_consecutive, still_interval, size = None):
        self.start_time = time.time()
        self.motion_threshold = motion_threshold
        self.min_blocks = min_blocks
        self.min_consecutive = min_consecutive
        self.still_interval = still_interval

        self.last_motion = None
        self.last_recordable = None
        self.warmed_up = False
        self.preview_running = False
        self.consecutive_motions = 0

        super().__init__(camera, size)

    def analyse(self, a):
        if self.warmed_up:
            a = np.sqrt(
                np.square(a['x'].astype(np.float)) +
                np.square(a['y'].astype(np.float))
            ).clip(0, 255).astype(np.uint8)
            # If there're more than 10 vectors with a magnitude greater
            # than 60, then say we've detected motion
            moving = (a > self.motion_threshold).sum()
            t = time.time()

            # Turn on the display at the slightest sign of motion,
            # then turn it off after 7 seconds of no motion
            if moving > 1:
                self.last_motion = t
                if not self.preview_running:
                    camera.start_preview()
                    self.preview_running = True
            elif self.preview_running and self.last_motion is not None and t - self.last_motion > 7:
                camera.stop_preview()
                self.preview_running = False

            # If at least min_blocks are moving for at least min_consecutive frames in a row,
            # signal that we can start recording.
            if moving > self.min_blocks:
                self.consecutive_motions += 1
                if (self.consecutive_motions >= self.min_consecutive):
                    self.last_recordable = t
            else:
                self.consecutive_motions = 0
                if (self.last_recordable is not None and
                    t - self.last_recordable > 2 * self.still_interval):
                    self.last_recordable = None
        else:
            # Warmup time needed to prevent spurious recording at start
            self.warmed_up = time.time() - self.start_time > 2


if __name__ == '__main__':
    dir = '/dev/shm/motion_capture'
    if not os.path.isdir(dir):
        os.mkdir(dir)
    
    wait_interval = 0.1 # how long to wait between checking for motion
    still_interval = 0.5 # min seconds between still frames
    framerate = 15
    camera_width = 1296
    camera_height = 730
    motion_width = 432
    motion_height = 243
    motion_threshold = 7
    min_blocks = 4
    min_consecutive = 2
    quality = 85
    iso = 800
    hflip = True
    vflip = False

    last_still = time.time()

    with picamera.PiCamera() as camera:
        camera.resolution = (camera_width, camera_height)
        camera.framerate = framerate
        camera.hflip = hflip
        camera.vflip = vflip
        camera.iso = iso
        with DetectMotion(camera, motion_threshold, min_blocks, min_consecutive, still_interval,
                          size=(motion_width, motion_height)) as output:
            camera.start_recording('/dev/null', resize=(motion_width, motion_height),
                                   format='h264', motion_output=output)
            while True:
                camera.wait_recording(wait_interval)
                if (output.last_recordable is not None
                    and time.time() - last_still >= still_interval):
                    time_now = datetime.datetime.now()
                    filename = '%s/picam-%s.jpg' % (dir, time_now.strftime('%FT%H-%M-%S.%f'))
                    camera.capture(filename, use_video_port=True, quality = quality)
                    last_still = time.time()
            camera.stop_recording()
