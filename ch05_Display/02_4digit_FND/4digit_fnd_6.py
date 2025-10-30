# file: 4digit_fnd_6.py

from gpiozero import LEDCharDisplay, LEDMultiCharDisplay
from time import sleep
from datetime import datetime

display = LEDCharDisplay(20, 21, 19, 13, 6, 16, 12, dp=26)
multi_display = LEDMultiCharDisplay(display, 23, 24, 25, 5)

print('Press Ctrl+C to exit')
print('-'*30)

while True:
    current_time = datetime.now().strftime('%H%M')
    multi_display.value = current_time
    print(f'Displaying: {current_time}')

    sleep(60)
