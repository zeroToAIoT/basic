# file: LightSensor_4.py

from gpiozero import LEDBarGraph, MCP3008
from time import sleep

mcp = MCP3008(channel=2)
led_bar = LEDBarGraph(17, 27, 22, 13, 19, pwm=True)

print('Press Ctrl+C to exit')

while True:
    led_bar.value = 1 - mcp.value
    print(f'Light value: {mcp.value:.3f}')
    
    sleep(1)