# file: led_button_6.py

from gpiozero import LED, Button
from signal import pause

leds = [LED(17), LED(27), LED(22)]
buttons = [Button(23, bounce_time=0.1), Button(24, bounce_time=0.1), Button(25, bounce_time=0.1)]

print('Press Ctrl+C to exit')

for button, led in zip(buttons, leds):
    button.when_pressed = led.on
    button.when_released = led.off

pause()