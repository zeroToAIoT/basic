# file: sound_3.py

from gpiozero import MCP3008, LED
from time import sleep

mcp = MCP3008(channel=5)
led = LED(17)
threshold = 0.7  

print('Press Ctrl+C to exit')

while True:
    if mcp.value > threshold:
        led.on()
        print(f'sound level is {mcp.value:.3f}, LED on')
    else:
        led.off()
        print(f'sound level is {mcp.value:.3f}, LED off')
    sleep(0.5)