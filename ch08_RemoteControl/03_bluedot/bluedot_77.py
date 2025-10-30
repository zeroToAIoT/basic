# file: bluedot_5.py

from bluedot import BlueDot
from gpiozero import LED
from signal import pause

red_led = LED(17)
green_led = LED(27)
bd = BlueDot()

def led_on():
    red_led.on()
    green_led.on()
    print('LED ON')

def led_off():
    led.off()
    print('LED OFF')

bd.when_pressed = led_on
bd.when_released = led_off

print('Waiting for BlueDot button press...')

try:
    pause()
except KeyboardInterrupt:
    print('stopped.. ctrl + c. ')
finally:
    led.off()
    print('finished...')