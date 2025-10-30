# file: Joystick_1.py

from gpiozero import MCP3008
from time import sleep

mcp_x = MCP3008(channel=6)
mcp_y = MCP3008(channel=7)

print('Press Ctrl+C to exit')

while True:
    print(f'X axis: {mcp_x.value:.3f}, Y axis: {mcp_y.value:.3f}')

    sleep(0.5)