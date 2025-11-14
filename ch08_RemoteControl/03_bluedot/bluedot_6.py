# file: bluedot_6.py

from bluedot import BlueDot
from gpiozero import LED
from signal import pause

red_led = LED(17)
green_led = LED(27)

bd = BlueDot(cols=2, rows=2)    # 2x2 버튼 생성

def button_pressed(btn):
    actions = {
        (0, 0): lambda: (red_led.on(), print('red_led_on')),
        (1, 0): lambda: (red_led.off(), print('red_led_off')),
        (0, 1): lambda: (green_led.on(), print('green_led_on')),
        (1, 1): lambda: (green_led.off(), print('green_led_off')),
    }
    
    action = actions.get((btn.col, btn.row))
    if action:
        action()
    else:
        print("Unknown button")

bd.when_pressed = button_pressed

print('BlueDot 2x2 Grid Button')
print('Waiting for button press...')
print('-'*30)

try:
    pause()
    
except KeyboardInterrupt:
    print('stopped.. ctrl + c. ')
finally:
    print('Bluetooth server closed.')
