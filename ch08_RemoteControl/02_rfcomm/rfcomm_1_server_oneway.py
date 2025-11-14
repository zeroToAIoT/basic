# file: rfcomm_1_server_oneway.py

import bluetooth
from time import sleep

client_sock = None
server_sock = None

try:
    # 1. create Bluetooth socket
    server_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    server_sock.setsockopt(bluetooth.SOL_SOCKET, bluetooth.SO_REUSEADDR, 1)

    # 2. set channel port 1
    port = 1
    server_sock.bind(('', port))
    server_sock.listen(1)

    # 3. advertise Bluetooth service
    uuid = '00001101-0000-1000-8000-00805F9B34FB' # standard Serial Port UUID
    bluetooth.advertise_service(
        server_sock,
        'zeroToAI_Server',  # name displayed in smartphone app
        service_id=uuid,
        service_classes=[uuid, bluetooth.SERIAL_PORT_CLASS],
        profiles=[bluetooth.SERIAL_PORT_PROFILE],
    )

    print(f'Waiting for Bluetooth connection on channel {port}...')
    print('Please run "sudo bluetoothctl discoverable on"')

    # 4. accept connection
    client_sock, client_info = server_sock.accept()
    print(f'Smartphone connected: {client_info[0]}')

    # 5. receive data
    print('Waiting for message from smartphone...')
    data = client_sock.recv(1024)

    if data:
        print(f'Received: {data.decode("utf-8")}')
    else:
        print('No data, connection is lost.')

    print('5 seconds later, the server will be closed.')
    sleep(5)

except KeyboardInterrupt:
    print('\nServer stopped by user (Ctrl+C).')

except bluetooth.btcommon.BluetoothError as bt_err:
    print(f'Bluetooth Error: {bt_err}')

except Exception as err:
    print(f'An unexpected error occurred: {err}')

finally:
    print('Cleaning up resources...')
    if client_sock:
        client_sock.close()
    if server_sock:
        server_sock.close()
    
    print('Finished server.')
