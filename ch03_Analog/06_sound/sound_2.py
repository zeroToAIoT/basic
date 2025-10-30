# file: sound_2.py

from gpiozero import MCP3008
from time import sleep

mcp = MCP3008(channel=5)

print('Press Ctrl+C to exit')

while True:
    print(f'mcp value : {mcp.value :.3f}')

    if mcp.value > 0.7:
        print('sound level is high')
    elif mcp.value < 0.3:
        print('sound level is low')
    else:
        print('sound level is medium')

    sleep(0.5)