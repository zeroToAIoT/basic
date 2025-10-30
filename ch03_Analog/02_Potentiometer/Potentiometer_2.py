# file: Potentiometer_2.py

from gpiozero import MCP3008, PWMLED
from time import sleep

mcp = MCP3008(channel=1)
led = PWMLED(17)

print('Press Ctrl+C to exit')

while True:
    print(f'{mcp.value :.3f}')
    led.source = mcp.value

    sleep(0.1)