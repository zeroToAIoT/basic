# file: PWMLED_5.py

from gpiozero import PWMLED
from time import sleep

ledRed = PWMLED(17)
ledOrange = PWMLED(27)
ledGreen = PWMLED(22)

print('Press Ctrl+C to exit')

while True:
    for i in range(256):  
        ledRed.value = i / 255
        ledOrange.value = (255 - i) / 255
        ledGreen.value = abs((i % 128) - 64) / 64
        sleep(0.03)