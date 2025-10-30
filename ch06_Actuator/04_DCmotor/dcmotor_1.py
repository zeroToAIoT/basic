# file: dcmotor_1.py

from gpiozero import Motor

Motor1 = Motor(forward=6, backward=13)

print('Press Ctrl+C to exit')

while True:
    Motor1.forward()
