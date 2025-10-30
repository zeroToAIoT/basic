# file: temp_2.py

from gpiozero import MCP3008
from time import sleep

mcp = MCP3008(channel=3)
max_volt = 5.0       		# 5.0 or 3.3

print('Press Ctrl+C to exit')

while True:
    mcp_volt = mcp.value * max_volt
    temp = (mcp_volt - 0.5) * 100       #TMP36 25C 0.5V

    print(f'Temperature : {temp:.1f} C')
    sleep(1)