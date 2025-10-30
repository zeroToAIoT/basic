# file: camera_5.py

from picamera2 import Picamera2, Preview
from time import sleep
import os

cam = Picamera2()

config = cam.create_still_configuration(
    main={
        'size':(1920, 1080),
        'format':'RGB888',
    }
)
cam.configure(config)

cam.start_preview(Preview.QTGL)
cam.start()
sleep(5)

save_dir = '/home/pi/basic/images'  # image save directory   
os.makedirs(save_dir, exist_ok=True)

INTERVAL = 5    # 5 seconds

counter = 1   # image counter

print('Press Ctrl+C to exit')
print('-'*30)

while True:
    filename = os.path.join(save_dir, f'img_{counter:03d}.jpg')
    cam.capture_file(filename)
    print(f'Captured {filename}')
    counter += 1
    sleep(INTERVAL)