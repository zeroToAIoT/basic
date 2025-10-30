# file: Joystick_2.py

from gpiozero import MCP3008, LED, Button
from signal import pause

mcp_x = MCP3008(channel=6)
mcp_y = MCP3008(channel=7)
sw = Button(12)
# sw = Button(12, pull_up=False) 
led = LED(17)

def button_pressed():
    print('button pressed. LED on!!!')
    led.on()

def button_released():
    print('button released. LED off!!')
    led.off()

print('Press Ctrl+C to exit')

sw.when_pressed = button_pressed
sw.when_released = button_released

pause()