# file: button_6.py

from gpiozero import Button
from signal import pause

btn1 = Button(23, bounce_time=0.1)
btn2 = Button(24, bounce_time=0.1)
btn3 = Button(25, bounce_time=0.1)

def btn1_pressed():
    print('Button 1 was pressed')

def btn2_pressed():
    print('Button 2 was pressed')

def btn3_pressed():
    print('Button 3 was pressed')

print('Press Ctrl+C to exit')

btn1.when_pressed = btn1_pressed
btn2.when_pressed = btn2_pressed
btn3.when_pressed = btn3_pressed

pause()