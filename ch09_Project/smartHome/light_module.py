# file: light_module.py

from gpiozero import MCP3008
from config import MCP3008_CHANNEL

# get the MCP3008 channel for the light sensor
light_sensor = MCP3008(channel=MCP3008_CHANNEL['LIGHT_SENSOR'])

def read_light_value():
    try:
        light_value = light_sensor.value
        print(f'Light Value: {light_value:8f}')
        return light_value
    except Exception as err:
        print(f'LightSensor Error : {err}')
        return None