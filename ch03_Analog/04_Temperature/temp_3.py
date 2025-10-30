# file: temp_2.py

from gpiozero import MCP3008
from time import sleep

mcp = MCP3008(channel=3)
max_volt = 5.0       		# 5.0 or 3.3

def get_temperature(mcp_value):
    mcp_volt = mcp_value * max_volt
    temp = (mcp_volt - 0.5) * 100
    return temp

print('Press Ctrl+C to exit')

while True:
    temp = get_temperature(mcp.value)
    
    print(f'mcp value: {mcp.value:.3f} , temperature: {temp:.1f} C')
    sleep(1)