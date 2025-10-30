# file: dcmotor_5.py

from gpiozero import Robot
from time import sleep

robot = Robot(left=(6, 13), right=(12, 16))

print('Press Ctrl+C to exit')
print('-'*30)

while True:
    print('Robot left')
    robot.left(speed=0.7)
    sleep(3)

    print('Robot stop')
    robot.stop()
    sleep(2)

    print('Robot right')
    robot.right(speed=0.7)
    sleep(3)

    print('Robot stop')
    robot.stop()
    sleep(2)