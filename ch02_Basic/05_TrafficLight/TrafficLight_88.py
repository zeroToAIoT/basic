# file: TrafficLight_88.py

from gpiozero import TrafficLights
from time import sleep
from signal import pause

light = TrafficLights(17, 27, 22)

def traffic_light():
    while True:
        print('Green light ON')
        yield (0, 0, 1)
        sleep(10)

        print('Amber light ON')
        yield (0, 1, 0)
        sleep(1)

        print('Red light ON')
        yield (1, 0, 0)
        sleep(10)

        print('Red + Amber light ON')
        yield (1, 1, 0)
        sleep(1)

light.source = traffic_light()

pause()