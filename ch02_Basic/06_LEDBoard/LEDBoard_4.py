# file: LEDBoard_4.py

from gpiozero import LEDBoard
from signal import pause
import random
from threading import Timer

leds = LEDBoard(17, 27, 22, 13, 19, pwm=True)

def update_leds():
    num_leds = random.randint(1, len(leds))
    selected_leds = random.sample(list(leds), num_leds)

    for led in selected_leds:
        brightness = random.uniform(0, 1)
        led.value = brightness
        print(f'LED on GPIO {led.pin.number}, brightness {brightness:.2f}')

    Timer(1, update_leds).start()

print('Press Ctrl+C to exit')

update_leds()

pause()