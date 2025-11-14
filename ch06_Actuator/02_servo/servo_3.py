# file: servo_3.py

from gpiozero import AngularServo
from time import sleep

servo = AngularServo(18, min_angle=-90, max_angle=90)

servo_angle = [0, 45, 90, 45, 0, -45, -90, -45, 0]

print('Press Ctrl+C to exit')
print('-'*30)

while True:
    for angle in servo_angle:
        print(f'Servo angle: {angle}')
        servo.angle = angle
        sleep(1)
    
    servo_angle.reverse()
