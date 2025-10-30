# file: led_button_2.py

from gpiozero import LED, Button
from signal import pause

ledRed = LED(17)
btnRed = Button(23, bounce_time=0.1)

print('Press Ctrl+C to exit')

btnRed.when_pressed = ledRed.on
btnRed.when_released = ledRed.off

pause()