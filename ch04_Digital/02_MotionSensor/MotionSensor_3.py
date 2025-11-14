# file: MotionSensor_3.py

from gpiozero import MotionSensor, LED
from signal import pause

pir = MotionSensor(25)
red_led = LED(17)
green_led = LED(27)

red_led.off()
green_led.on()

def motion_detected():
    red_led.on()
    green_led.off()
    print('Motion detected: red_led ON, green_led OFF')
    
def no_motion_detected():
    red_led.off()
    green_led.on()
    print('No motion detected: red_led OFF, green_led ON')

print('Press Ctrl+C to exit')
print('-'*30)

pir.when_motion = motion_detected
pir.when_no_motion = no_motion_detected

pause()