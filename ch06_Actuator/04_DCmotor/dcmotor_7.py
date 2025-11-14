# file: dcmotor_7.py

from gpiozero import Robot, Button
from signal import pause

robot= Robot(left=(6, 13), right=(12, 16))

btn1 = Button(17, bounce_time=0.1)
btn2 = Button(27, bounce_time=0.1)
btn3 = Button(22, bounce_time=0.1)

btn1.when_pressed = robot.forward
btn2.when_pressed = robot.stop
btn3.when_pressed = robot.backward

pause()