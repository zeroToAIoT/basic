# file: rfcomm_3_server_led.py

import bluetooth
from gpiozero import LED

led = LED(17) # 17번 핀에 연결된 LED
port = 1
server_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
# ... (bind, listen, advertise 설정은 동일) ...

print('LED 제어 서버 시작. (채널 1)')
print('스마트폰에서 \'on\' 또는 \'off\'를 보내세요...')

try:
    client_sock, client_info = server_sock.accept()
    print(f'스마트폰 연결 성공: {client_info[0]}')
    client_sock.send('RPi: LED Control Ready.\n'.encode('utf-8'))

    while True:
        data = client_sock.recv(1024)
        if not data:
            break

        # 수신된 명령어를 소문자로 변환
        command = data.decode('utf-8').strip().lower() 
        print(f'스마트폰 (RX): [ {command} ]')

        if command == 'on':
            led.on()
            response = 'RPi: LED ON\n'
        elif command == 'off':
            led.off()
            response = 'RPi: LED OFF\n'
        elif command == 'quit':
            response = 'RPi: Bye!\n'
        else:
            response = 'RPi: Unknown command (try \'on\' or \'off\')\n'
        
        client_sock.send(response.encode('utf-8'))
        
        if command == 'quit':
            break

except Exception as err:
    print(f'Error: {err}')
    
finally:
    print('Closing server.')
    if 'client_sock' in locals():
        client_sock.close()
    if 'server_sock' in locals():
        server_sock.close()
    print('Finished server.')