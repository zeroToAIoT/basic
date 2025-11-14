# file: servo_4.py

from gpiozero import AngularServo, Button
from signal import pause

servo = AngularServo(18, min_angle=-90, max_angle=90)

btn1 = Button(17, bounce_time=0.1)
btn2 = Button(27, bounce_time=0.1)
btn3 = Button(22, bounce_time=0.1)

def move_to_min():
    servo.angle = -90
    print('Servo moved to -90°')

def move_to_mid():
    servo.angle = 0
    print('Servo moved to 0°')

def move_to_max():
    servo.angle = 90
    print('Servo moved to 90°')

print('Press Ctrl+C to exit')
print('-'*30)

btn1.when_pressed = move_to_min
btn2.when_pressed = move_to_mid
btn3.when_pressed = move_to_max

pause()