# file: bluetooth_rfcomm_2_pc_1.py

import serial

bt = None

try:
    bt = serial.Serial('COM5', baudrate=9600, timeout=1.0)
    print('Bluetooth connection successful!')
    print('-' * 30)

    while True:
        # 사용자로부터 메시지 입력받기
        message = input("Enter message to send (or 'quit' to exit): ")
        
        if message.lower() == 'quit':
            print("Exiting...")
            break
        
        # 메시지 전송
        bt.write(f'{message}\n'.encode('utf-8'))
        print(f"Sent: {message}")
        
        # 응답 받기
        response = bt.readline().decode('utf-8').strip()
        if response:
            print(f"Received from Pi: {response}")
        else:
            print("No response from Pi.")
        
        print("-" * 30)

except serial.SerialException as e:
    print(f'Bluetooth error: {e}')

except Exception as err:
    print(f'Error: {err}')

finally:
    if bt and bt.is_open:
        bt.close()
        print('Bluetooth connection closed.')
