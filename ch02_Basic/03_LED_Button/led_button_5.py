# file: led_button_5.py

from gpiozero import LED, Button
from signal import pause

ledRed = LED(17)
ledOrange = LED(27)
ledGreen = LED(22)

btnRed = Button(23, bounce_time=0.1)
btnOrange = Button(24, bounce_time=0.1)
btnGreen = Button(25, bounce_time=0.1)

print('Press Ctrl+C to exit')

ledRed.source = btnRed
ledOrange.source = btnOrange
ledGreen.source = btnGreen

pause()