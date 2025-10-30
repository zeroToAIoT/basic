# file: 4digit_fnd_4.py

from gpiozero import LEDCharDisplay, LEDMultiCharDisplay
from time import sleep

display = LEDCharDisplay(20, 21, 19, 13, 6, 16, 12, dp=26)
multi_display = LEDMultiCharDisplay(display, 23, 24, 25, 5)

text = 'ILOVEYOU!!'

print('Press Ctrl+C to exit')
print('-'*30)

while True:
    for i in range(len(text) - 3):
        multi_display.value = text[i:i+4]
        sleep(0.3)

    sleep(1)