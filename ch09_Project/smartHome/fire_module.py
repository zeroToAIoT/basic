# file: fire_module.py
# Fire Detection Module

from gpiozero import MCP3008
from config import THRESHOLDS, MCP3008_CHANNEL
import led_module, buzzer_module

fire_sensor = MCP3008(MCP3008_CHANNEL['FIRE_SENSOR'])

def read_fire_value():
    try:
        fire_level = fire_sensor.value
        print(f'Fire Sensor Value: {fire_level:.2f}')
        return fire_level
    except Exception as err:
        print(f'Fire Sensor Error: {err}')
        return None

def fire_detect():
    fire_level = read_fire_value()
    
    if fire_level is not None and fire_level > THRESHOLDS['FIRE_HIGH']:
        print('Fire detected! Alerting system...')
        led_module.by_fire(True)
        buzzer_module.by_fire(True)
        return True
    else:
        print('No fire detected.')
        led_module.by_fire(False)
        buzzer_module.by_fire(False)
        return False