# file: button_1.py

from gpiozero import Button
from signal import pause

btn1 = Button(23)

print('Press Ctrl+C to exit')

while True:
    btn1.wait_for_press()
    print('Button pressed')

pause()