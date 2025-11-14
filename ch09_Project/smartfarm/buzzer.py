# file: buzzer.py
# Buzzer Control Module

from time import sleep
from gpiozero import Buzzer
from config import PIN, get_threshold

buzzer = Buzzer(PIN['BUZZER'])

def play_melody(melody):
    """공통 멜로디 재생 함수"""
    for duration in melody:
        buzzer.on()
        sleep(duration)
        buzzer.off()
        sleep(0.1)

def warning_beep():
    """짧은 경고음 (기본 알람)"""
    play_melody([0.2, 0.2])

def melody_fan():
    play_melody([0.2, 0.2, 0.3, 0.3, 0.4, 0.4])

def melody_moisture():
    play_melody([0.1, 0.3, 0.2, 0.4, 0.2, 0.3])

def melody_water_tank():
    play_melody([0.3, 0.2, 0.4, 0.2, 0.3, 0.1])

def check_and_alert(temp, hum, moisture, water_level):
    """센서 값 확인 후 상황별 경고음 발생"""
    try:
        # Temperature and humidity alerts
        if temp is not None and hum is not None:
            if temp <= get_threshold('temp_low') or hum <= get_threshold('hum_low'):
                warning_beep()

        # Moisture alert → 전용 멜로디
        if moisture is not None and moisture <= get_threshold('moisture_low'):
            melody_moisture()

        # Water level alert → 전용 멜로디
        if water_level is not None and water_level <= get_threshold('water_low'):
            melody_water_tank()

    except Exception as err:
        print(f'Error in buzzer control: {err}')

def buzzer_cleanup():
    buzzer.off()
    buzzer.close()