# file: water_44.py

from gpiozero import OutputDevice, MCP3008
from time import sleep

mcp = MCP3008(channel=4)

pump = OutputDevice(18)

max_volt = 5.0
max_level_cm = 100  # 최대 수위 (예: 100cm)


def get_water_level(value):
    voltage = value * max_volt
    return (voltage / max_volt) * max_level_cm  # 센서 값 → 수위 변환

try:
    while True:
        water_level = get_water_level(mcp.value)  # 수위 값 변환

        # 펌프 자동 제어
        if water_level <= 20:
            pump.on()  # 수위 낮으면 펌프 가동
        elif water_level >= 50:
            pump.off()  # 수위 충분하면 펌프 중지

        print(f'Water Level: {water_level:.2f} cm | Pump: {\'ON\' if water_level <= 20 else \'OFF\'}')

        sleep(1)  # 1초 간격으로 확인
except KeyboardInterrupt:
    print('\n프로그램 종료')
    pump.off()  # 프로그램 종료 시 펌프 OFF