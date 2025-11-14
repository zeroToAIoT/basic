# file: dcmotor_4.py

from gpiozero import Robot
from time import sleep

robot = Robot(left=(6, 13), right=(12, 16))

print('Press Ctrl+C to exit')
print('-'*30)

while True:
    print('Robot forward')
    robot.forward(speed=1)
    sleep(3)

    print('Robot stop')
    robot.stop()
    sleep(2)

    print('Robot backward')
    robot.backward(speed=0.5)
    sleep(3)