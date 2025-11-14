# file: TrafficLight_4.py

from gpiozero import TrafficLights
from time import sleep

light = TrafficLights(17, 27, 22)

def change_light(color, duration, message):
    color.on()
    print(message)
    sleep(duration)
    color.off()

print('Press Ctrl+C to exit')

while True:
    change_light(light.green, 5, 'Green ON, GO!!')
    change_light(light.amber, 1, 'Amber ON, SLOW DOWN!!')
    change_light(light.red, 5, 'Red ON, STOP!!')
