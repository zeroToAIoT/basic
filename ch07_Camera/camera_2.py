# file: camera_2.py

from picamera2 import Picamera2, Preview
from time import sleep

cam = Picamera2()

cam.start_preview(Preview.QTGL)  # OpenGL preview window
cam.start()
sleep(5)

cam.capture_file('camera_preview_test.jpg')

cam.stop_preview()

cam.close()