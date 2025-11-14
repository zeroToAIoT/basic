# file: camera_module.py
# Camera Capture Module

from picamera2 import Picamera2
from datetime import datetime
import os

DIR = 'capture/'
os.makedirs(DIR, exist_ok=True)

home_cam = Picamera2()
home_cam.configure(home_cam.create_still_configuration())

def capture_image(location):
    try:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'{DIR}{location}_{timestamp}.jpg'

        home_cam.start_and_capture(filename)
        
        print(f'Image captured : {filename}')
        return filename

    except Exception as err:
        print(f'Error capturing image: {err}')
        return None
    finally:
        home_cam.stop()

def cleanup():
    """리소스 정리 함수"""
    global home_cam
    try:
        if home_cam:
            home_cam.stop()
            home_cam.close()
        print("Camera module cleaned up.")
    except Exception as e:
        print(f"Camera module cleanup error: {e}")