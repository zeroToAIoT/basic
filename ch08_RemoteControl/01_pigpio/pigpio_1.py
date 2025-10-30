# file: pigpio_1.py

from gpiozero.pins.pigpio import PiGPIOFactory

ip = '192.168.1.77'
remotePi = PiGPIOFactory(host=ip)

try:
    if remotePi.connected:
        print('Connected to the Raspberry Pi')
    else:
        print('Not connected to the Raspberry Pi')

except KeyboardInterrupt:
    print('Stopped by Ctrl+C.')
except Exception as err:
    print(f'Error : {err}')

finally:
    remotePi.close()
    print('Connection closed')