# file: PWMLED_2.py

from gpiozero import PWMLED
from time import sleep

ledRed = PWMLED(17)
ledOrange = PWMLED(27)
ledGreen = PWMLED(22)

print('Press Ctrl+C to exit')

while True:
	ledRed.value = 0
	ledOrange.value = 0
	ledGreen.value = 0
	sleep(0.5)
	
	ledRed.value = 0.5
	ledOrange.value = 0.5
	ledGreen.value = 0.5
	sleep(0.5)

	ledRed.value = 1
	ledOrange.value = 1
	ledGreen.value = 1
	sleep(0.5)