# file: led_5.py

from gpiozero import LED
from random import randint
from signal import pause

led1 = LED(17)
led2 = LED(27)

def rand():
    while True:
        yield randint(0, 1)

print('Press Ctrl+C to exit')

led1.source_delay = 0.5
led1.source = rand()

led2.source_delay = 0.5
led2.source = rand()

pause()