# file: led_3.py

from gpiozero import LED
from signal import pause

led1 = LED(23)
led2 = LED(24)

print('Press Ctrl+C to exit')

led1.blink(on_time=1, off_time=0.5)
led2.blink(on_time=1, off_time=0.5)

pause()