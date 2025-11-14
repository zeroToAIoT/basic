# file: sound_4.py

from gpiozero import MCP3008, LED
from signal import pause

mcp = MCP3008(channel=5)
led = LED(17)
threshold = 0.7  

def control_led():
    while True:
        print(f'mcp value: {mcp.value:.3f}')
        
        if mcp.value > threshold:
            yield 1  
        else:
            yield 0  

print('Press Ctrl+C to exit')

led.source = control_led()
led.source_delay = 0.5

pause()