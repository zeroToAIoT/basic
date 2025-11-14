# file: LineSensor_3.py

from gpiozero import LineSensor, LED
from signal import pause

line = LineSensor(12)
red_led = LED(17)
green_led = LED(27)

def on_line():
    print('black_1')
    red_led.on()
    green_led.off()

def off_line():
    print('white_0')
    red_led.off()
    green_led.on()

print('Press Ctrl+C to exit')
print('-'*30)

line.when_line = on_line
line.when_no_line = off_line

pause()
