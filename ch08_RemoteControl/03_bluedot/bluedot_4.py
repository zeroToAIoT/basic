# file name: bluedot_4.py

from bluedot import BlueDot
from signal import pause

bd = BlueDot(cols=2, rows=2)    # 2x2 버튼 생성

def button_pressed(btn):
    messages = {
        (0, 0): 'red_led_on',
        (1, 0): 'red_led_off',
        (0, 1): 'green_led_on',
        (1, 1): 'green_led_off',

    }
    print(messages.get((btn.col, btn.row), "Unknown"))

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
