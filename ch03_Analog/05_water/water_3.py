# file: water_3.py

from gpiozero import MCP3008
from time import sleep

mcp = MCP3008(channel=4)
max_volt = 5.0
full_level = 100.0

def get_water_level(value, full_level):
    mcp_volt = value * max_volt
    water_level = (mcp_volt / max_volt) * full_level
    return water_level

print('Press Ctrl+C to exit')

while True:
    water_level = get_water_level(mcp.value, full_level)   
    
    print(f'mcp value: {mcp.value:.3f} , Water Level: {water_level:.1f}%')
    sleep(1)