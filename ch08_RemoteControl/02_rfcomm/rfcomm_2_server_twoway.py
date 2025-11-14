# file: rfcomm_2_server_twoway.py

import bluetooth
from datetime import datetime

try:
    # 1. set up Bluetooth socket (RFCOMM protocol)
    server_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    server_sock.setsockopt(bluetooth.SOL_SOCKET, bluetooth.SO_REUSEADDR, 1)

    port = 1  # use channel port 1
    server_sock.bind(('', port))
    server_sock.listen(1)

    # 2. advertise Bluetooth service
    uuid = '00001101-0000-1000-8000-00805F9B34FB'  # 표준 Serial Port UUID

    bluetooth.advertise_service(
        server_sock,
        'zeroToAI_Server',  # name displayed in smartphone app
        service_id=uuid,
        service_classes=[uuid, bluetooth.SERIAL_PORT_CLASS],
        profiles=[bluetooth.SERIAL_PORT_PROFILE],
    )

    print(f'Start Bluetooth RFCOMM two-way server on channel {port}...')
    print('Please connect with Serial Bluetooth Terminal app on smartphone...')

    # 3. wait for client connection
    print('Waiting for client connection...')
    client_sock, client_info = server_sock.accept()
    print(f'Smartphone connected: {client_info}')

    # 4. two-way communication loop
    while True:
        data = client_sock.recv(1024)

        if not data:
            print('Smartphone connection is lost.')
            break

        # 받은 데이터(bytes)를 문자열(string)로 변환
        received_message = data.decode('utf-8').strip()

        # print the received string in Raspberry Pi terminal
        print(f'Smartphone (RX): [ {received_message} ]')

        # 5. generate response (TX) based on the received message
        if received_message.lower() == 'quit':
            print('Received quit command. Closing connection.')
            client_sock.send('RPi: Bye!\n'.encode('utf-8'))
            break
        elif received_message.lower() == 'time':
            now = datetime.now().strftime('%H:%M:%S')
            response = f'RPi: The time is {now}\n'
        else:
            response = f'RPi: You sent [{received_message}]\n'

        # 6. send response message to smartphone
        client_sock.send(response.encode('utf-8'))
        print(f'  -> Response (TX) sent: [ {response.strip()} ]')

except KeyboardInterrupt:
    print('User terminated the program.')
except Exception as err:
    print(f'Error: {err}')

finally:
    # 7. close all sockets
    print('Closing server.')
    if 'client_sock' in locals():
        client_sock.close()
    if 'server_sock' in locals():
        server_sock.close()
    print('Finished server.')