# file: LEDBarGraph_1.py

from gpiozero import LEDBarGraph
from time import sleep

ledBar = LEDBarGraph(17, 27, 22, 13, 19)

print('Press Ctrl+C to exit')

while True:
	ledBar.value = 0		# (0, 0, 0, 0, 0)		# Off
	sleep(1)
	ledBar.value = 1/5		# (1, 0, 0, 0, 0)		# one LED on
	sleep(1)
	ledBar.value = 2/5		# (1, 1, 0, 0, 0)		# two LEDs on
	sleep(1)
	ledBar.value = 3/5		# (1, 1, 1, 0, 0)		# three LEDs on
	sleep(1)
	ledBar.value = 4/5		# (1, 1, 1, 1, 0)		# four LEDs on
	sleep(1)
	ledBar.value = 1		# (1, 1, 1, 1, 1)		# five LEDs on
	sleep(1)