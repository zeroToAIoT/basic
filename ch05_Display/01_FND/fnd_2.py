# file: fnd_2.py

from gpiozero import LEDCharDisplay
from signal import pause

display = LEDCharDisplay(20, 21, 19, 13, 6, 16, 12, dp=26)

print('Press Ctrl+C to exit')

display.source_delay = 1
display.source = '0123456789'

pause()