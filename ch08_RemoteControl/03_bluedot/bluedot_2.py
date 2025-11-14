# file: bluedot_2.py

from bluedot import BlueDot
from signal import pause

bd = BlueDot(cols=2, rows=1)			#버튼 2개 (왼쪽, 오른쪽)

def button_pressed(button):
    if button.col == 0:
        print('hello')
    elif button.col == 1:
        print('bye')

bd.when_pressed = button_pressed

print('left button is "hello", right button is "bye"')
print('-'*30)

try:
    pause()

except KeyboardInterrupt:
    print('stopped.. ctrl + c. ')
finally:
    print('Bluetooth server closed.')
