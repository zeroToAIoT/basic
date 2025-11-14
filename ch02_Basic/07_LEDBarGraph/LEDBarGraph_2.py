# file: LEDBarGraph_2.py

from gpiozero import LEDBarGraph
from time import sleep

ledBar = LEDBarGraph(17, 27, 22, 13, 19)
DELAY = 0.5

print('Press Ctrl+C to exit')

while True:
    for i in range(6):
        ledBar.value = i / 5 
        sleep(DELAY)