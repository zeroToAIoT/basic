# file: LightSensor_2.py

from gpiozero import MCP3008
from time import sleep

mcp = MCP3008(channel=2)

print('Press Ctrl+C to exit')

while True:
    if mcp.value < 0.5:
        print(f'Dart!!, value : {mcp.value:.3f}')
    else:
        print(f'Light!!, value : {mcp.value:.3f}')
    
    sleep(1)