# file: LineSensor_1.py

from gpiozero import LineSensor
from time import sleep

line = LineSensor(12)

print('Press Ctrl+C to exit')
print('-'*30)

while True:
	if line.value == 1:
		print('black_1')
	else: 
		print('white_0')

	sleep(1)
