# file: bluedot_5.py
# refer : bluedot_3.py

from bluedot import BlueDot
from gpiozero import LED

red_led = LED(17)
green_led = LED(27)
bd = BlueDot(cols=2, rows=2)    # 2x2 버튼 생성

print('BlueDot 2x2 Grid Button')
print('Waiting for button press...')
print('-'*30)

try:
    while True:
        bd[0, 0].wait_for_press()
        print('red_led_on')
        red_led.on()

        bd[1, 0].wait_for_press()
        print('red_led_off')
        red_led.off()

        bd[0, 1].wait_for_press()
        print('green_led_on')
        green_led.on()
        
        bd[1, 1].wait_for_press()
        print('green_led_off')
        green_led.off()

except KeyboardInterrupt:
    print('stopped.. ctrl + c. ')
finally:
    print('Bluetooth server closed.')
