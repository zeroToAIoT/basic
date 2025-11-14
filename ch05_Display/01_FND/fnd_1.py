# file: fnd_1.py

from gpiozero import LEDCharDisplay
from signal import pause

display = LEDCharDisplay(20, 21, 19, 13, 6, 16, 12, dp=26)
#display = LEDCharDisplay(20, 21, 19, 13, 6, 16, 12, dp=26, active_high=False)

print('Press Ctrl+C to exit')

display.source_delay = 1
display.source ='8FAH'

pause()