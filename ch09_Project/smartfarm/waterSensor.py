# file: waterSensor.py
# Water Tank Level Sensor Module

from gpiozero import MCP3008
from config import MCP

water_sensor = MCP3008(channel=MCP['WATER_SENSOR'])

def read_water_level():
    try:
        water = water_sensor.value

        if water is None:
            print('[WaterSensor] Invalid water level reading')
            return None

        # 0~1 범위를 0~100%로 변환
        water_percent = water * 100

        print(f'[WaterSensor] Level: {water_percent:.2f}%')
        return water_percent

    except Exception as err:
        print(f'[WaterSensor Error] {err}')
        return None