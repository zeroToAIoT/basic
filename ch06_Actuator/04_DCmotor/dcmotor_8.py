# file: dcmotor_7_1.py

from gpiozero import Robot, Button
from signal import pause

robot = Robot(left=(6, 13), right=(12, 16))

btn1 = Button(17, bounce_time=0.1)
btn2 = Button(27, bounce_time=0.1)
btn3 = Button(22, bounce_time=0.1)

def move_forward():
    print('Moving forward')
    robot.forward(speed=1)

def stop_robot():
    print('Stopping')
    robot.stop()

def move_backward():
    print('Moving backward')
    robot.backward(speed=0.5)

btn1.when_pressed = move_forward
btn2.when_pressed = stop_robot
btn3.when_pressed = move_backward

pause()