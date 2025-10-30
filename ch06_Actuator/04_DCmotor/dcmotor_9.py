# file: dcmotor_9.py

from gpiozero import Robot, DistanceSensor
from signal import pause

dis = DistanceSensor(23, 24, max_distance=1, threshold_distance=0.2)
robot = Robot(left=(5, 6), right=(25, 16))

def forward(speed):
    robot.forward(speed)

def backward(speed):
    robot.backward(speed)

def stop():
    robot.stop()

def object_detected():
    print('Object detected')
    stop()
    robot.backward(speed=0.5)

def object_not_detected():
    print('Object not detected')
    print('Moving forward')
    forward(speed=1.0)

print('Distance Sensor Activate')
print('Press Ctrl+C to exit')
print('-'*30)

dis.when_in_range = object_detected
dis.when_out_of_range = object_not_detected

pause()