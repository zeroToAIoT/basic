# file: button_3.py

from gpiozero import Button
from time import sleep

btn1 = Button(23)

print('Press Ctrl+C to exit')

while True:
    if btn1.is_pressed:
        print('Button1 is pressed')
    else:
        print('Button1 is not pressed')
    sleep(2) 