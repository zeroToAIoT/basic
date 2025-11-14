# file: light.py
# Light Sensor Module

from config import MCP
from gpiozero import MCP3008

light_sensor = MCP3008(channel=MCP['LIGHT_SENSOR'])

def read_light_sensor():
    try:
        light_value = light_sensor.value

        if light_value is None:
            print('[Light] Invalid reading')
            return None

        # 0~1 범위를 0~100%로 변환
        light_percent = light_value * 100

        print(f'[Light] Value: {light_percent:.2f}%')
        return light_percent

    except Exception as err:
        print(f'[Light Error] {err}')
        return None

def light_cleanup():
    light_sensor.close()