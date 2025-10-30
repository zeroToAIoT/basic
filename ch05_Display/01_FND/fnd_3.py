# file: fnd_3.py

from gpiozero import LEDCharDisplay
from time import sleep

display = LEDCharDisplay(20, 21, 19, 13, 6, 16, 12, dp=26)

print('Press Ctrl+C to exit')

while True:
    for i in range(10):
        display.value = str(i)
        sleep(1)