# file: morningCall_module.py

import pygame
import random
from datetime import datetime
from time import sleep
import os
from system_status import is_system_active

MUSIC_DIR = 'music/'
os.makedirs(MUSIC_DIR, exist_ok=True)

def morningCall_play():
    try:
        files = [f for f in os.listdir(MUSIC_DIR) if f.endswith('.mp3')]
        if not files:
            print(f'No music files found in {MUSIC_DIR}')
            return
        
        MUSIC_FILE = os.path.join(MUSIC_DIR, random.choice(files))

        pygame.mixer.init()
        pygame.mixer.music.load(MUSIC_FILE)
        pygame.mixer.music.set_volume(0.5)

        while is_system_active():
            now = datetime.now()
            if now.hour == 6 and now.minute == 0:
                pygame.mixer.music.play(-1)
                print(f'Morning call music started: {MUSIC_FILE}')

            sleep(60)

    except KeyboardInterrupt:
        print('Morning call stopped.. ctrl+c pressed')
    except Exception as e:
        print(f'Error : {e}') 
    finally:
        pygame.mixer.music.stop()
        pygame.mixer.quit()

def cleanup():
    """리소스 정리 함수"""
    try:
        pygame.mixer.music.stop()
        pygame.mixer.quit()
        print("MorningCall module cleaned up.")
    except Exception as e:
        print(f"MorningCall module cleanup error: {e}")