# file: servo_1.py

from gpiozero import Servo
from time import sleep

servo = Servo(18)

while True:
	servo.min()		#servo.value=0.0
	sleep(1)
	servo.mid()  	#servo.value=0.5
	sleep(1)
	servo.max()		#servo.value=1.0
	sleep(1)
	servo.mid()		#servo.value=0.5
	sleep(1)
	servo.min()		#servo.value=0.0
	sleep(1)