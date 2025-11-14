# file: TrafficLight_99.py

from gpiozero import TrafficLights
from time import sleep

light = TrafficLights(17, 27, 22)

def change_light(color, duration, name):
    color.on()
    print(f'{name} light ON')
    sleep(duration)
    color.off()
    print(f'{name} light OFF')
    sleep(0.5)

try:
    while True:
        change_light(light.red, 1, 'Red')
        change_light(light.amber, 1, 'Amber')
        change_light(light.green, 1, 'Green')
except KeyboardInterrupt:
    print('Program finished')