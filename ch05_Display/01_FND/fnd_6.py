# file: fnd_6.py

from gpiozero import LEDCharDisplay
from time import sleep

display = LEDCharDisplay(20, 21, 19, 13, 6, 16, 12, dp=26)
pattern = ['Z', 'E', 'R', 'O', 'T', 'O', 'A', 'I'] 
#pattern = ['P', 'H', 'Y', 'S', 'I', 'C', 'A', 'L', 'A', 'I'] 

print('Press Ctrl+C to exit')

while True:
    for char in pattern:
        display.value = char
        sleep(0.3)
    
    sleep(1)