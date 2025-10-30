# file: Potentiometer_3.py

from gpiozero import MCP3008, RGBLED
from time import sleep

mcp = MCP3008(channel=1)
rgbled = RGBLED(13, 19, 26)

print('Press Ctrl+C to exit')

while True:
    print(f'{mcp.value :.3f}')
    red = mcp.value
    green = 1 - mcp.value
    blue = 0.5

    rgbled.color = (red, green, blue)
    
    sleep(0.1)