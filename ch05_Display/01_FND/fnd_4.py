# file: fnd_4.py

from gpiozero import LEDCharDisplay
from time import sleep
import random

display = LEDCharDisplay(20, 21, 19, 13, 6, 16, 12, dp=26)

print('Press Ctrl+C to exit')

while True:
    random_number = random.randint(0, 9)
    
    display.value = random_number
    
    sleep(3)