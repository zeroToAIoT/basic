# file: moisture.py
# Moisture Sensor Module using MCP3008

from gpiozero import MCP3008
from config import MCP

moisture_sensor = MCP3008(channel=MCP['MOISTURE_SENSOR'])

def read_moisture():
    try:
        moi = moisture_sensor.value

        if moi is None:
            print('[Moisture] Invalid reading')
            return None

        # 0~1 범위를 0~100%로 변환
        moisture_percent = moi * 100

        print(f'[Moisture] Value: {moisture_percent:.2f}%')
        return moisture_percent

    except Exception as err:
        print(f'[Moisture Error] {err}')
        return None

def moisture_cleanup():
    moisture_sensor.close()