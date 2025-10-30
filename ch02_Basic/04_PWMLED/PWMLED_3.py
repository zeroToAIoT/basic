# file: PWMLED_3.py

from gpiozero import PWMLED
from signal import pause

ledRed = PWMLED(17)
ledOrange = PWMLED(27)
ledGreen = PWMLED(22)

print('Press Ctrl+C to exit')

ledRed.pulse()
ledOrange.pulse()
ledGreen.pulse()

pause()