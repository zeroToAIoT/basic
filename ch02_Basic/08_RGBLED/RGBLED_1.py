# file: RGBLED_1.py

from gpiozero import RGBLED
from time import sleep

rgbled = RGBLED(16, 20, 21)

print('Press Ctrl+C to exit')

while True:
    rgbled.red = 1      # Red
    sleep(1)
    rgbled.green = 1      # Green
    sleep(1)
    rgbled.blue = 1      # Blue
    sleep(1)