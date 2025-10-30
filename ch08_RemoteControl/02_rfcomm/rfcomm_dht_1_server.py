# file: rfcomm_dht_1_server.py

import bluetooth
import board
import adafruit_dht
from time import sleep

# create a Bluetooth server to send DHT11 sensor data
server_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
server_sock.bind(('', bluetooth.PORT_ANY))
server_sock.listen(1)
port = server_sock.getsockname()[1]

print(f'Waiting for Bluetooth connection on RFCOMM channel {port}...')
client_sock, client_info = server_sock.accept()
print(f'Connected to {client_info}')

dht = adafruit_dht.DHT11(board.D21, use_pulseio=False)

try:
    while True:
        temp = dht.temperature
        hum = dht.humidity

        if temp is not None and hum is not None:
            data = f'Temperature: {temp:.1f}C, Humidity: {hum:.1f}%'
            client_sock.send(data)
            print(f'Sent: {data}')
        sleep(2)

except KeyboardInterrupt:
    print('Server Stopped. Ctrl+C pressed.')
except OSError:
    print('Connection error occurred. Disconnecting.')
except Exception as err:
    print(f'Error : {err}')

finally:
    client_sock.close()
    server_sock.close()
    print('Bluetooth server closed.')
    dht.exit()