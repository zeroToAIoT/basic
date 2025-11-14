# file: button_2.py

from gpiozero import Button
from signal import pause

btn2 = Button(24)

def btn_pressed():
    print('Button2 was pressed')

print('Press Ctrl+C to exit')

btn2.when_pressed = btn_pressed

pause()