# file: MotionSensor_1.py

from gpiozero import MotionSensor
from time import sleep

pir = MotionSensor(25)

print('Press Ctrl+C to exit')
print('-'*30)

while True:   
    if pir.motion_detected:
        print('Motion detected')
    else:
        print('No motion detected')

    sleep(1)
