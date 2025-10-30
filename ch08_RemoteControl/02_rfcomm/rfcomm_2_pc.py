# file: bluetooth_rfcomm_2_pc.py

import serial

bt = None

print('Bluetooth connection started...')
print('Press Ctrl+C to exit')
print('-' * 30)

try:
    bt = serial.Serial('COM5', baudrate=9600, timeout=1.0)
    print('Bluetooth connection successful!')
    print('-' * 30)

    bt.write(b'Hello, pi!\n')
    response = bt.readline().decode('utf-8').strip()
    if response:
        print(f'Received from Pi: {response}')
    else:
        print('No response from Pi.')

except serial.SerialException as e:
    print(f'Bluetooth error: {e}')

except Exception as err:
    print(f'Error: {err}')

finally:
    if bt and bt.is_open:
        bt.close()
        print('Bluetooth connection closed.')
