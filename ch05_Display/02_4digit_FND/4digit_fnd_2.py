# file: 4digit_fnd_2.py

from gpiozero import LEDCharDisplay, LEDMultiCharDisplay
from time import sleep

display = LEDCharDisplay(20, 21, 19, 13, 6, 16, 12, dp=26)
multi_display = LEDMultiCharDisplay(display, 23, 24, 25, 5)

words = ['1234', 'ZERO', '8888', 'LIFE']

print('Press Ctrl+C to exit')
print('-'*30)

while True:
     for word in words:
         multi_display.value = word
         print(f'Displaying: {word}')
         sleep(2)
