# file: PWMLED_4.py

from gpiozero import PWMLED
from time import sleep

ledRed = PWMLED(17)
ledOrange = PWMLED(27)
ledGreen = PWMLED(22)

print('Press Ctrl+C to exit')

while True:
    for i in range(256):
        value = i / 255
        ledRed.value = value
        ledOrange.value = value
        ledGreen.value = value
        sleep(0.03)

    for i in range(256):
        value = (255 - i) / 255
        ledRed.value = value
        ledOrange.value = value
        ledGreen.value = value
        sleep(0.03)