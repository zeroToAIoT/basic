# file: camera_4_2.py

from picamera2 import Picamera2, Preview
from time import sleep
import os

cam = Picamera2()

config = cam.create_still_configuration(
    main={
        'size':(1920, 1080),
        'format':'RGB888',
    },
    lores={
        'size':(640, 480),
        'format':'BGR888',
    },
    controls={
        'ExposureTime': 10000,      # 10 ms
        'AnalogueGain': 1.4
    }
)

cam.configure(config)

save_dir = '/home/pi/basic/images'
os.makedirs(save_dir, exist_ok=True)

cam.start_preview(Preview.QTGL)  # OpenGL preview window

cam.start()
sleep(5)

filename = os.path.join(save_dir, 'test.png')
cam.capture_file(filename)

cam.stop_preview()
cam.close()

print(f'Saved as {filename}')