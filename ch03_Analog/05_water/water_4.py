# file: water_4.py

from gpiozero import MCP3008, LED
from time import sleep

mcp = MCP3008(channel=4)
led = LED(17)
max_volt = 5.0
full_level = 100.0
threshold = 20.0

def get_water_level(value, full_level):
    mcp_volt = value * max_volt
    water_level = (mcp_volt / max_volt) * full_level
    return water_level

print('Press Ctrl+C to exit')

while True:
    water_level = get_water_level(mcp.value, full_level)

    if water_level < threshold:
        led.on()
        print(f'water level is low {water_level:.1f}%, LED on')
    else:
        led.off()
        print(f'water level is high {water_level:.1f}%, LED off')
    
    sleep(1)