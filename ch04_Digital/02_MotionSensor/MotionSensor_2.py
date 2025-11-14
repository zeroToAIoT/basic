# file: MotionSensor_2.py

from gpiozero import MotionSensor
from signal import pause

pir = MotionSensor(25)

def motion_detected():
    print('Motion detected')

def no_motion_detected():
    print('No motion detected')

print('Press Ctrl+C to exit')
print('-'*30)

pir.when_motion = motion_detected
pir.when_no_motion = no_motion_detected

pause()