# file: RGBLED_2.py

from gpiozero import RGBLED
from time import sleep

rgbled = RGBLED(16, 20, 21)

print('Press Ctrl+C to exit')

while True:
    rgbled.color=(0, 0, 0)		# off, black
    sleep(1)
    rgbled.color=(1, 0, 0)		# red
    sleep(1)
    rgbled.color=(1, 1, 0)		# yellow
    sleep(1)
    rgbled.color=(0, 1, 0)		# green
    sleep(1)
    rgbled.color=(0, 0, 1)		# blue
    sleep(1)
    rgbled.color=(0, 1, 1)		# cyan
    sleep(1)
    rgbled.color=(1, 0, 1)		# magenta
    sleep(1)
    rgbled.color=(1, 1, 1)		# white
    sleep(1)