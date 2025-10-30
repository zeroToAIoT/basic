# file: led_button_4.py

from gpiozero import LED, Button
from signal import pause

ledRed = LED(17)
btnRed = Button(23, bounce_time=0.1)

def toggle_and_print():
    ledRed.toggle()
    print(f'LED is now {'ON' if ledRed.value else 'OFF'}')

print('Press Ctrl+C to exit')

btnRed.when_pressed = toggle_and_print

pause()