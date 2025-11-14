# file: button_5.py

from gpiozero import Button
from signal import pause

btn1 = Button(23)

def hi():
    print('Hi. everyone!!')

def bye():
    print('Bye. see you again')

print('Press Ctrl+C to exit')

btn1.when_pressed = hi
btn1.when_released = bye

pause()