# file: LEDBarGraph_4.py

from gpiozero import LEDBarGraph
from time import sleep
from random import choice

ledBar = LEDBarGraph(17, 27, 22, 13, 19)
DELAY = 0.5

patterns = [0.2, 0.4, 0.6, 0.8, 1]

print('Press Ctrl+C to exit')

while True:
    random_pattern = [choice(patterns) for _ in range(5)]
    ledBar.value = random_pattern
    sleep(DELAY)

    for led in ledBar:
        led.off()
        sleep(DELAY)
