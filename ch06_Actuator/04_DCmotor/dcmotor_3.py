# file: dcmotor_3.py

from gpiozero import Motor
from time import sleep

Motor1 = Motor(forward=6, backward=13)
Motor2 = Motor(forward=12, backward=16)

print('Press Ctrl+C to exit')
print('-'*30)

while True:
    print('Motor1 forward, Motor2 forward')
    Motor1.forward()
    Motor2.forward()
    sleep(3)

    print('Motor1 stop, Motor2 stop')
    Motor1.stop()
    Motor2.stop()
    sleep(2)

    print('Motor1 backward, Motor2 backward')
    Motor1.backward(speed=0.5)
    Motor2.backward(speed=0.5)
    sleep(3)
