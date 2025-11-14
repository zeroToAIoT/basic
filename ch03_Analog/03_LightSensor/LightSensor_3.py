# file: LightSensor_3.py

from gpiozero import MCP3008, LED
from signal import pause

mcp = MCP3008(channel=2)
led = LED(17)
threshold = 0.2

def control():
    while True:
        print(f'Light value: {mcp.value:.3f}')
        yield 1 if mcp.value < threshold else 0 

print('Press Ctrl+C to exit')

led.source = control()
led.source_delay = 0.5

pause()