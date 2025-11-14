# libgpiod_2_led.py

from gpiozero.pins.native import NativeFactory
from gpiozero import LED
from time import sleep

remote_factory = NativeFactory(
    host='192.168.137.30', 
    user='pi', 
    password='12345678' 
    )

led = LED(17, pin_factory=remote_factory)

print('Connecting to the Raspberry Pi...')
print('Press Ctrl+C to exit')
print('-'*30)

try:
    if remote_factory.connected is None:
        print('Not connected to the Raspberry Pi')
    else:
        print('Connected to the Raspberry Pi')

        while True:
            led.on()
            sleep(1)
            led.off()
            sleep(1)

except Exception as err:
    print(f'Error : {err}')
    exit()

finally:
    remote_factory.close()