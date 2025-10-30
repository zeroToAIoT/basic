# file: LEDBoard_1.py

from gpiozero import LEDBoard
from time import sleep

leds = LEDBoard(17, 27, 22, 13, 19)

print('Press Ctrl+C to exit')

while True:
    leds.on()
    sleep(1)
    leds.off()
    sleep(1)

    leds.value=(1, 0, 0, 0, 0)      # Red
    sleep(0.5)
    leds.value=(0, 1, 0, 0, 0)      # Green
    sleep(0.5)
    leds.value=(0, 0, 1, 0, 0)      # Blue
    sleep(0.5)
    leds.value=(0, 0, 0, 1, 0)      # Yellow
    sleep(0.5)
    leds.value=(0, 0, 0, 0, 1)      # Purple
    sleep(0.5)

    leds.value=(0, 0, 0, 0, 0)      # Off
    sleep(1)