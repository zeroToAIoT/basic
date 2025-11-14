# file: RGBLED_4.py

from gpiozero import RGBLED
from time import sleep

rgbled = RGBLED(16, 20, 21)

def color_increase(target_color):
    for n in range(101):
        rgbled.color = (target_color[0] * (n / 100),
                        target_color[1] * (n / 100),
                        target_color[2] * (n / 100))
        sleep(0.1)

print('Press Ctrl+C to exit')

while True:
    color_increase((1, 0, 0))       # Red
    color_increase((0, 1, 0))       # Green
    color_increase((0, 0, 1))       # Blue