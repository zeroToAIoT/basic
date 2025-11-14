# libgpiod_1.py

from gpiozero.pins.native import NativeFactory

remote_factory = NativeFactory(
        host='192.168.137.30',
        user='pi',
        password='12345678'
    )

print('Connecting to the Raspberry Pi...')
print('Press Ctrl+C to exit')
print('-'*30)

try:
    if remote_factory.connected is None:
        print('Not connected to the Raspberry Pi')
    else:
        print('Connected to the Raspberry Pi')

except Exception as err:
    print(f'Error : {err}')
    exit()

finally:
    remote_factory.close()
