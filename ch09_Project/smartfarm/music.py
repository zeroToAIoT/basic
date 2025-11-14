# file: music.py
# Music Module for Plant Growth (every hour at the start of the hour)

import os
from time import sleep
from datetime import datetime
import pygame
  
from config import MUSIC_PATH
    
def get_music_files():
    music_files = []
    try:
        for filename in os.listdir(MUSIC_PATH):
            if filename.endswith(('.mp3', '.wav')):
                full_path = os.path.join(MUSIC_PATH, filename)
                music_files.append(full_path)
        return music_files
    except FileNotFoundError:
        print(f"Music folder not found: {MUSIC_PATH}")
        return []
  
def play_music_at_hour(music_files, now=None): 
    """정각에 한 번 음악을 재생하는 함수 (자동 제어용)"""
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
        else:
            # 정각이 아니면 아무것도 하지 않습니다.
            pass
    except Exception as err:
        print(f'Music play error: {err}')
  
def music_loop(stop_event, get_system_status_func): 
    try:
        music_files = get_music_files()
        
        pygame.mixer.init()
        pygame.mixer.music.set_volume(0.5)

        print("[Music] Music loop started, waiting for activation...")

        last_check_minute = -1 
        
        while not stop_event.is_set(): # stop_event가 set될 때까지 반복
            if get_system_status_func(): # 시스템이 활성화되어 있을 때만 작동
                now = datetime.now()
                # 매분 0초에만 play_music_at_hour를 호출하여 오작동 방지
                if now.minute != last_check_minute and now.second == 0:
                    play_music_at_hour(music_files, now) # 정각 체크 로직 포함된 함수 호출
                    last_check_minute = now.minute 
            else:
                # 시스템 비활성화 시 음악 정지
                if pygame.mixer.music.get_busy():
                    pygame.mixer.music.stop()
                    print("[Music] System deactivated, music stopped.")
            
            sleep(1) 
    except Exception as err:
        print(f'Music loop error: {err}')
    finally:
        if pygame.mixer.get_init():
            pygame.mixer.quit()
        print("[Music] Music loop stopped.")
  
_is_manual_music_playing = False # 수동 재생 상태 플래그

def start_music_manual(music_files=None): 
    """Start music manually (from BlueDot)"""
    global _is_manual_music_playing
    try:
        if _is_manual_music_playing:
            print("[Music] Manual music already playing.")
            return

        if music_files is None: 
            music_files = get_music_files()

        if not music_files:
            print('No music files available for manual play!')
            return

        pygame.mixer.init()
        pygame.mixer.music.set_volume(0.5)
        selected_music = music_files[0] 
        pygame.mixer.music.load(selected_music)
        pygame.mixer.music.play(-1) 
        _is_manual_music_playing = True
        print(f'[Music] Manually playing {selected_music}')
    except Exception as err:
        print(f'Error starting manual music: {err}')
  
def stop_music_manual(): 
    """Stop music manually (from BlueDot)"""
    global _is_manual_music_playing
    try:
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.stop()
            print('[Music] Music stopped manually')
        _is_manual_music_playing = False
    except Exception as err:
        print(f'Error stopping manual music: {err}')

def music_cleanup():
    if pygame.mixer.get_init():
        pygame.mixer.quit()
    print("[Music] Pygame mixer cleaned up.")