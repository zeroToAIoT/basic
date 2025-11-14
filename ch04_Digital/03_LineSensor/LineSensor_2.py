# file: LineSensor_2.py

from gpiozero import LineSensor
from signal import pause

line = LineSensor(12)

def on_line():
    print('black_1')

def off_line():
    print('white_0')

print('Press Ctrl+C to exit')
print('-'*30)

line.when_line = on_line
line.when_no_line = off_line

pause()