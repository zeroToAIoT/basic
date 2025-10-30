# file: bluedot_1.py

from bluedot import BlueDot
from signal import pause

def say_hello():
    print('hello !!')

bd = BlueDot()

bd.when_pressed = say_hello

print('Waiting for button press...')
print('-'*30)

try:
    pause()
    
except KeyboardInterrupt:
    print('stopped.. ctrl + c. ')
finally:
    print('Bluetooth server closed.')
