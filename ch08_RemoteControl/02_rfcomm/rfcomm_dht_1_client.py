# file: rfcomm_dht_1_client.py

import bluetooth

server_address = 'XX:XX:XX:XX:XX:XX'  # Raspberry Pi Bluetooth address

# create a Bluetooth client to connect to the server
client_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
client_sock.connect((server_address, 1))

print(f'Connected to Raspberry Pi at {server_address}')

try:
    while True:
        data = client_sock.recv(1024)
        if not data:
            break
        print(f'Received: {data.decode()}')

except KeyboardInterrupt:
    print('Client Stopped. Ctrl+C pressed.')
except Exception as err:
    print(f'Error : {err}')

finally:
    client_sock.close()
    print('Bluetooth connection closed.')