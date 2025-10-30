# file: led_button_1.py

from gpiozero import LED, Button
from time import sleep

ledRed = LED(17)
btnRed = Button(23, bounce_time=0.1)

print('Press Ctrl+C to exit')

while True:
    if btnRed.is_pressed:
        ledRed.on()
    else:
        ledRed.off()
    
    sleep(0.1)