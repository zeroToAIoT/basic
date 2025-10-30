# file: DistanceSensor_3.py

from gpiozero import DistanceSensor
from signal import pause

#ultra = DistanceSensor(echo=24, trigger=23)
ultra = DistanceSensor(24, 23, max_distance=1.0, threshold_distance=0.2)

def object_detected():
    print('Object detected')

def object_not_detected():
    print('Object not detected')

print('Press Ctrl+C to exit')
print('-'*30)

ultra.when_in_range = object_detected
ultra.when_out_of_range = object_not_detected

pause()