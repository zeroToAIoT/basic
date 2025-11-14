# file: temp_3.py

from gpiozero import LED, MCP3008
from time import sleep

mcp = MCP3008(channel=3)
max_volt = 5.0       		# 5.0 or 3.3
led = LED(17)

def get_temperature(mcp_value):
    mcp_volt = mcp_value * max_volt
    temp = (mcp_volt - 0.5) * 100        
    return temp

print('Press Ctrl+C to exit')

while True:
    temp = get_temperature(mcp.value)
    
    if temp >= 30:
        led.on()
        print(f'Temperature: {temp:.1f} C, LED on')
    else:
        led.off()
        print(f'Temperature: {temp:.1f} C, LED off')
    
    sleep(1)