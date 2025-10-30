# file: rfcomm_dht_2_client.py

import bluetooth

server_address = 'XX:XX:XX:XX:XX:XX'

client_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
client_sock.connect((server_address, 1))

print(f'Connected to Raspberry Pi at {server_address}')
print('-'*30)

try:
    while True:
        data = client_sock.recv(1024)
        if not data:
            break
        print(f'Received:{data.decode()}')
        print('-'*30)

except KeyboardInterrupt:
    print('Client Stopped. Ctrl+C pressed.')
except OSError:
    print('Connection error occurred. Disconnecting.')
except Exception as err:
    print(f'Error: {err}')

finally:
    client_sock.close()
    print('Bluetooth connection closed.')