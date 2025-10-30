# file: TrafficLight_3.py

from gpiozero import TrafficLights
from time import sleep

light = TrafficLights(17, 27, 22)

def change_light(color, duration):
    color.on()
    sleep(duration)
    color.off()

print('Press Ctrl+C to exit')

while True:
    change_light(light.green, 5)
    change_light(light.amber, 1)
    change_light(light.red, 5)


