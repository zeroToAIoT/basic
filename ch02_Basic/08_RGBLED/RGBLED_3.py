# file: RGBLED_3.py

from gpiozero import RGBLED
from time import sleep

rgbled = RGBLED(16, 20, 21)
DELAY = 1

colors = [
    (0, 0, 0),      # Off
    (1, 0, 0),      # Red
    (1, 1, 0),      # Yellow
    (0, 1, 0),      # Green
    (0, 0, 1),      # Blue
    (0, 1, 1),      # Cyan
    (1, 0, 1),      # Magenta
    (1, 1, 1),      # White
]

print('Press Ctrl+C to exit')

while True:
    for color in colors:
        rgbled.color = color
        print(f'LED color is {color}')
        sleep(DELAY)
