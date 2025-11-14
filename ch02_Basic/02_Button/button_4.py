# file: button_4.py

from gpiozero import Button
from signal import pause

btn1 = Button(23)

def on_press():
    print('Button pressed')

def on_release():
    print('Button is not pressed')

print('Press Ctrl+C to exit')

btn1.when_pressed = on_press
btn1.when_released = on_release

pause()