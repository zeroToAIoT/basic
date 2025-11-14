# file: water_2.py

from gpiozero import MCP3008
from time import sleep

mcp = MCP3008(channel=4)
max_volt = 5.0
full_level = 100.0

print('Press Ctrl+C to exit')

while True:
    mcp_volt = mcp.value * max_volt
    water_level = (mcp_volt / max_volt) * full_level    # 0 ~ 100

    print(f'water level : {water_level:.1f}%')
    sleep(0.5)
