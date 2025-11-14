# file: fnd_5.py

from gpiozero import LEDCharDisplay
from time import sleep

display = LEDCharDisplay(20, 21, 19, 13, 6, 16, 12, dp=26)
pattern = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'] 

print('Press Ctrl+C to exit')

while True:
    for char in pattern:
        display.value = char
        sleep(0.3)
    
    sleep(1)