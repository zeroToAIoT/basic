# file: led_module.py
# led control module

from gpiozero import LED
from config import THRESHOLDS, PIN
from light_module import read_light_value
from fire_module import fire_detect
from pir_module import pir_detect
led = LED(PIN['LED'])

def by_light():
    try:
        light_level = read_light_value()

        if light_level and light_level < THRESHOLDS['LIGHT_LOW']:
            print(f'Light level is {light_level:.2f}, Dark... Turning on LED.')
            led.on()
        elif light_level and light_level > THRESHOLDS['LIGHT_HIGH']:
            print(f'Light level is {light_level:.2f}, Bright.... Turning off LED.')
            led.off()
        else:
            print(f'Light level is {light_level:.2f}, Normal... Turning off LED.')
            led.off()
        return light_level

    except Exception as err:
        print(f'LED Control Error: {err}')

def by_fire():
    try:
        fire_detected = fire_detect()

        if fire_detected and fire_detected < THRESHOLDS['FIRE_LOW']:
            print(f'Fire level is {fire_detected:.2f}, Fire detected! Turning on LED.')
            led.blink(on_time=0.2, off_time=0.2)
        else:
            print(f'Fire level is {fire_detected:.2f}, No fire detected. Turning off LED.')
            led.off()
        return fire_detected
    
    except IOError as err:
        print(f'LED Control Error: {err}')
        return None

def by_pir():
    try:
        pir_detected = pir_detect()

        if pir_detected:
            print('Motion Detected.! Turning on LED.')
            led.blink(on_time=0.5, off_time=0.5)
        else:
            print('Nothing. Turning off LED.')
            led.off()
        return pir_detected
    
    except IOError as err:
        print(f'LED Control Error: {err}')
        return None