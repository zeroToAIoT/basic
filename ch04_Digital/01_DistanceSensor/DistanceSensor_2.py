# file: DistanceSensor_2.py

from gpiozero import DistanceSensor
from time import sleep

#ultra = DistanceSensor(echo=24, trigger=23)
ultra = DistanceSensor(24, 23)
i=0

print('Press Ctrl+C to exit')
print('-'*30)

while True:
    i+=1
    print(f'{i}. Distance : {ultra.distance :.3f} m')
    sleep(1)