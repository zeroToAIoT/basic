# file: temp_1.py

from gpiozero import MCP3008
from time import sleep

mcp = MCP3008(channel=3)

print('Press Ctrl+C to exit')

while True:
    print(f'mcp value : {mcp.value :.3f}')
        
    sleep(0.5)
