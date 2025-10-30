# file: dcmotor_6.py

from gpiozero import Robot
from time import sleep

robot = Robot(left=(6, 13), right=(12, 16))

def move_forward(speed, duration):
    print(f'Moving forward {speed}')
    robot.forward(speed=speed)
    sleep(duration)
    robot.stop()

def move_backward(speed, duration):
    print(f'Moving backward')
    robot.backward(speed=speed)
    sleep(duration)
    robot.stop()

def move_turn_left(speed, duration):
    print(f'Truning left')
    robot.left(speed=speed)
    sleep(duration)
    robot.stop()

def move_turn_right(speed, duration):
    print(f'Truning left')
    robot.right(speed=speed)
    sleep(duration)
    robot.stop()

print('Press Ctrl+C to exit')
print('-'*30)

while True:
    move_forward(speed=1.0, duration=2)  # 전진
    move_backward(speed=0.6, duration=2)  # 후진
    move_turn_left(speed=0.7, duration=2)  # 좌회전
    move_turn_right(speed=0.7, duration=2)  # 우회전
    robot.stop()
