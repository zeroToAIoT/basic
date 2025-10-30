# file: rfcomm_1_pi.py

import bluetooth

# RFCOMM 소켓 생성
server_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
server_sock.bind(("", bluetooth.PORT_ANY))   # 모든 인터페이스, 임의 포트
server_sock.listen(1)

port = server_sock.getsockname()[1]
print(f'RFCOMM server started (port {port})')

print('Waiting for client connection...')
client_sock, client_info = server_sock.accept()
print('Connected to:', client_info)

try:
    while True:
        data = client_sock.recv(1024)   # 데이터 수신
        if not data:
            break
        msg = data.decode().strip()
        print('Message received from PC:', msg)

        # 클라이언트로 응답 보내기
        response = f'PC. You sent this message: {msg}'
        client_sock.send(response.encode())

except OSError:
    print('Connection error occurred. Disconnecting.')

finally:
    client_sock.close()
    server_sock.close()
    print('Disconnected.')