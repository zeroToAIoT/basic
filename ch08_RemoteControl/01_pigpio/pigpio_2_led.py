# file: pigpio_2_led.py
# refer : ch02_Basic/01_LED/led_2.py

from time import sleep
from gpiozero import LED
from gpiozero.pins.pigpio import PiGPIOFactory


ip = '192.168.137.161'          # Raspberry Pi IP address
remotePi = PiGPIOFactory(host=ip)

led1 = LED(17, pin_factory=remotePi)
led2 = LED(27, pin_factory=remotePi)

print('Press Ctrl+C to exit')
print('-'*30)

try:
    while True:
        led1.on()
        led2.on()
        print('LED ON')
        sleep(1)

        led1.off()
        led2.off()
        print('LED OFF')
        sleep(1)

except KeyboardInterrupt:
    print('Stopped by Ctrl+C.')
except Exception as err:
    print(f'Error : {err}')

finally:
    remotePi.close()
    print('Finished.')