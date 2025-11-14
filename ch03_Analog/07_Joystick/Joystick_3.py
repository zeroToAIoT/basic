# file: Joystick_3.py

from gpiozero import MCP3008
from time import sleep

mcp_x = MCP3008(channel=6)
mcp_y = MCP3008(channel=7)

print('Press Ctrl+C to exit')

while True:
    x = mcp_x.value
    y = mcp_y.value
    
    if x < 0.3 and y < 0.3:
        pos = 'Left-Down'
    elif 0.3 <= x <= 0.7 and y < 0.3:
        pos = 'Down'
    elif x > 0.7 and y < 0.3:
        pos = 'Right-Down'
    elif x < 0.3 and 0.3 <= y <= 0.7:
        pos = 'Left'
    elif 0.3 <= x <= 0.7 and 0.3 <= y <= 0.7:
        pos = 'Center'
    elif x > 0.7 and 0.3 <= y <= 0.7:
        pos = 'Right'
    elif x < 0.3 and y > 0.7:
        pos = 'Left-Up'
    elif 0.3 <= x <= 0.7 and y > 0.7:
        pos = 'Up'
    elif x > 0.7 and y > 0.7:
        pos = 'Right-Up'
    
    print(f'X axis: {x:.3f}, Y axis: {y:.3f}, Position: {pos}')
    sleep(0.5)