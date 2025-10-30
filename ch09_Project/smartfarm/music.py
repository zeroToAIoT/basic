# file: music.py
# Music Module for Plant Growth (every hour at the start of the hour)

import os
from time import sleep
from datetime import datetime
import pygame
# import random

from config import MUSIC_PATH
from main import get_system_status

# Get music file list
def get_music_files():
    music_files = []
    try:
        for filename in os.listdir(MUSIC_PATH):
            # Check if the file extension is .mp3 or .wav
            if filename.endswith(('.mp3', '.wav')):
                full_path = os.path.join(MUSIC_PATH, filename)
                music_files.append(full_path)
        return music_files
    except FileNotFoundError:
        print(f"Music folder not found: {MUSIC_PATH}")
        return []

def play_music(music_files, now=None):
    try:
        if now is None:
            now = datetime.now()

        if now.minute == 0 and now.second == 0:
            pygame.mixer.init()
            pygame.mixer.music.set_volume(0.5)
            print(f'[{now.strftime("%H:%M")}] Music play started.')

            if music_files:
                selected_music = music_files[now.hour % len(music_files)]
                # selected_music = random.choice(music_files)
                pygame.mixer.music.load(selected_music)
                pygame.mixer.music.play()
                print(f'[{now.strftime("%H:%M")}] Playing {selected_music}')
            else:
                print('No music files available!')
    except Exception as err:
        print(f'Music play error: {err}')

def music_loop():
    try:
        music_files = get_music_files()
        pygame.mixer.init()
        pygame.mixer.music.set_volume(0.5)
        while get_system_status():
            now = datetime.now()
            play_music(music_files, now)
            sleep(1)
    except Exception as err:
        print(f'Music loop error: {err}')

# Manual control functions for BlueDot
def start_music():
    """Start music loop"""
    try:
        music_files = get_music_files()
        pygame.mixer.init()
        pygame.mixer.music.set_volume(0.5)
        print('Music system started')
    except Exception as e:
        print(f'Error starting music: {e}')

def stop_music():
    """Stop music"""
    try:
        pygame.mixer.music.stop()
        print('Music stopped')
    except Exception as e:
        print(f'Error stopping music: {e}')