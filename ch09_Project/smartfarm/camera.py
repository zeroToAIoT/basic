# file: camera.py
# Capture Image Module for Plant Growth Monitoring using Picamera2

import os
from datetime import datetime
from time import sleep
from picamera2 import Picamera2
from config import CAMERA_RESOLUTION, CAMERA_FRAMERATE


def capture_image(image_path):
    """단일 이미지 캡처 (예외적 상황에서 사용)"""
    try:
        os.makedirs(image_path, exist_ok=True)  # 저장 경로 보장

        picam2 = Picamera2()
        config = picam2.create_still_configuration(main={"size": CAMERA_RESOLUTION})
        picam2.configure(config)
        picam2.start()

        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        file_path = os.path.join(image_path, f'imagePlant_{timestamp}.jpg')

        picam2.capture_file(file_path)
        print(f"[Camera] Image captured successfully: {file_path}")

        picam2.close()
        return file_path

    except Exception as err:
        print(f"[Camera Error] Capture Error: {err}")
        return None


def capture_image_loop(stop_event, image_path, interval):
    """주기적으로 이미지 캡처 (권장 방식)"""
    os.makedirs(image_path, exist_ok=True)  # 저장 경로 보장

    picam2 = Picamera2()
    config = picam2.create_still_configuration(main={"size": CAMERA_RESOLUTION})
    picam2.configure(config)
    picam2.start()

    try:
        while not stop_event.is_set():
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            file_path = os.path.join(image_path, f'imagePlant_{timestamp}.jpg')

            picam2.capture_file(file_path)
            print(f"[Camera] Image captured successfully: {file_path}")

            # interval 동안 1초 단위로 stop_event 확인
            for _ in range(interval):
                if stop_event.is_set():
                    break
                sleep(1)

    except Exception as err:
        print(f"[Camera Error] Capture Loop Error: {err}")
    finally:
        picam2.close()
        print("[Camera] Camera released.")
