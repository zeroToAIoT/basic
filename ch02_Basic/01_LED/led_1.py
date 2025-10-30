# file : led_1.py

from gpiozero import LED
from time import sleep

led1 = LED(17)

print('Press Ctrl+C to exit')

while True:
    led1.on()
    sleep(1)
    led1.off()
    sleep(1)