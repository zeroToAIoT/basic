# file: rfcomm_dht_2_server.py

import bluetooth
import board
import adafruit_dht
from gpiozero import LED
from gpiozero.pins.pigpio import PiGPIOFactory
from time import sleep

ip = '192.168.137.161'          # Raspberry Pi IP address
remotePi = PiGPIOFactory(host=ip)

dht = adafruit_dht.DHT11(board.D21, use_pulseio=False)
red_led = LED(17, pin_factory=remotePi)
green_led = LED(27, pin_factory=remotePi)

server_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
server_sock.bind(('', bluetooth.PORT_ANY))
server_sock.listen(1)

print('Press Ctrl+C to exit')
print('-'*30)

print('Waiting for Bluetooth connection...')
client_sock, client_info = server_sock.accept()
print(f'Connected to {client_info}')

try:
    while True:
        temp = dht.temperature
        hum = dht.humidity

        if temp is not None and hum is not None:
            print(f'Temperature: {temp:.1f}C, Humidity: {hum:.1f}%')

            if temp >= 30:
                red_led.on()
                temp_status = 'High Temperature → Red LED ON'
            else:
                red_led.off()
                temp_status = 'Normal Temperature'

            if hum >= 70:
                green_led.on()
                hum_status = 'High Humidity → Green LED ON'
            else:
                green_led.off()
                hum_status = 'Normal Humidity'

            data = f'{temp_status}\n{hum_status}\nTemp: {temp:.1f}C, Hum: {hum:.1f}%'
            client_sock.send(data)
            print(f'Sent: {data}')

        sleep(2)

except KeyboardInterrupt:
    print('Server Stopped. Ctrl+C pressed.')
except OSError:
    print('Connection error occurred. Disconnecting.')
except Exception as err:
    print(f'Error: {err}')

finally:
    red_led.off()
    green_led.off()
    dht.exit()
    client_sock.close()
    server_sock.close()
    remotePi.close()
    print('Bluetooth server closed.')