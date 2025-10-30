# file: dcmotor_2.py

from gpiozero import Motor

Motor2 = Motor(forward=12, backward=16)

print('Press Ctrl+C to exit')

while True:
    Motor2.forward()
