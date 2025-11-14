# file: rfcomm_4_server_dht.py

import bluetooth
import adafruit_dht
import board
from time import sleep

try:
    # DHT11 센서 초기화
    dht = adafruit_dht.DHT11(board.D21, use_pulseio=False)
    
    # 블루투스 소켓 설정
    server_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    server_sock.setsockopt(bluetooth.SOL_SOCKET, bluetooth.SO_REUSEADDR, 1)
    server_sock.bind(('', 1))
    server_sock.listen(1)

    # 블루투스 서비스 광고
    uuid = '00001101-0000-1000-8000-00805F9B34FB'
    bluetooth.advertise_service(
        server_sock,
        'DHT11_Server',
        service_id=uuid,
        service_classes=[uuid, bluetooth.SERIAL_PORT_CLASS],
        profiles=[bluetooth.SERIAL_PORT_PROFILE],
    )

    print('DHT11 블루투스 서버 시작...')
    print('스마트폰에서 연결하세요...\n')

    # 클라이언트 연결 대기
    client_sock, client_info = server_sock.accept()
    print(f'스마트폰 연결됨: {client_info}\n')

    # 5초 간격으로 센서 데이터 전송
    while True:
        try:
            temperature = dht.temperature
            humidity = dht.humidity
            message = f'Temperature: {temperature}C, Humidity: {humidity}%\n'
            
            client_sock.send(message.encode('utf-8'))
            print(f'Sent: {message.strip()}')
            
            sleep(5)  # 5초 대기
            
        except RuntimeError as err:
            print(f'Sensor error: {err}')
            sleep(5)

except KeyboardInterrupt:
    print('\nProgram terminated.')
except Exception as err:
    print(f'Error: {err}')

finally:
    if 'dht' in locals():
        dht.deinit()
    if 'client_sock' in locals():
        client_sock.close()
    if 'server_sock' in locals():
        server_sock.close()
