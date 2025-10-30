# file: rfcomm_phone_2_server.py

import bluetooth

server_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
server_sock.bind(('', bluetooth.PORT_ANY))
server_sock.listen(1)

print('Waiting for Bluetooth connection...')
client_sock, client_info = server_sock.accept()
print(f'Connected to {client_info}')

try:
    while True:
        # 데이터 수신
        data = client_sock.recv(1024)
        if not data:
            break
        print(f'Received: {data.decode()}')
        
        # 응답 전송
        response = input("Send message: ")
        client_sock.send(response.encode())
        
except KeyboardInterrupt:
    print('Server stopped.')
finally:
    client_sock.close()
    server_sock.close()