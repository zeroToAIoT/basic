# file: led_4.py

from gpiozero import LED
from random import randint
from time import sleep

led1 = LED(17)
led2 = LED(27)

print('Press Ctrl+C to exit')

while True:
    led1.value = randint(0, 1)
    led2.value = randint(0, 1)
    
    sleep(1)