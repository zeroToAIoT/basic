# file: 4digit_fnd_3.py

from gpiozero import LEDCharDisplay, LEDMultiCharDisplay
from time import sleep

display = LEDCharDisplay(20, 21, 19, 13, 6, 16, 12, dp=26)
multi_display = LEDMultiCharDisplay(display, 23, 24, 25, 5)

words = ['AI', 'ZERO', 'TOAI', 'AIOT', 'GPIO', 'ADC', 'FND', 'FARM', 'HOME', 'CODE']

print('Press Ctrl+C to exit')

while True:
    for word in words:
        multi_display.value = word
        print(f'Displaying: {word}')
        sleep(2)