# file: rfcomm_5_server_dht_led.py

import bluetooth
import adafruit_dht
import board
from time import sleep
from gpiozero import LED

led = LED(17) 

try:
    dht = adafruit_dht.DHT11(board.D21, use_pulseio=False)
    
    server_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    server_sock.setsockopt(bluetooth.SOL_SOCKET, bluetooth.SO_REUSEADDR, 1)
    server_sock.bind(('', 1))
    server_sock.listen(1)
  
    uuid = '00001101-0000-1000-8000-00805F9B34FB'
    bluetooth.advertise_service(
        server_sock,
        'DHT_LED_Server', 
        service_id=uuid,
        service_classes=[uuid, bluetooth.SERIAL_PORT_CLASS],
        profiles=[bluetooth.SERIAL_PORT_PROFILE],
    )
  
    print('DHT11 & LED Bluetooth Server started...')
    print('Connect your phone...\n')
  
    client_sock, client_info = server_sock.accept()
    print(f'Phone connected: {client_info[0]}\n') 
    
    client_sock.send('Server: Connected. Send "on", "off" to control LED.\n'.encode('utf-8'))
  
    last_dht_send_time = time.time() 
    
    while True:
        try:
            client_sock.settimeout(0.1) 
            received_data = client_sock.recv(1024)
            if received_data:
                command = received_data.decode('utf-8').strip().lower()
                print(f'Phone (RX): [ {command} ]')

                response_message = ''
                if command == 'on':
                    led.on()
                    response_message = 'Server: LED is now ON.\n'
                elif command == 'off':
                    led.off()
                    response_message = 'Server: LED is now OFF.\n'
                elif command == 'quit':
                    response_message = 'Server: Disconnecting. Bye!\n'
                    client_sock.send(response_message.encode('utf-8'))
                    break 
                else:
                    response_message = f'Server: Unknown command [{command}]. Try "on" or "off".\n'
                
                client_sock.send(response_message.encode('utf-8'))
                print(f'  -> Response (TX): [ {response_message.strip()} ]')

        except bluetooth.btcommon.BluetoothError as e:
            if "timed out" not in str(e): 
                print(f"Bluetooth receive error: {e}")
            pass 
        except Exception as e:
            print(f"Command processing error: {e}")

        current_time = time.time()
        if current_time - last_dht_send_time >= 5:
            try:
                temperature = dht.temperature
                humidity = dht.humidity
                message = f'Temperature: {temperature}C, Humidity: {humidity}%\n'
                
                client_sock.send(message.encode('utf-8'))
                print(f'Sent DHT: {message.strip()}')
                
            except RuntimeError as err:
                print(f'DHT sensor error: {err}')
            
            last_dht_send_time = current_time 
        
        sleep(0.01) 
  
except KeyboardInterrupt:
    print('\nProgram terminated (Ctrl+C).')
except Exception as err:
    print(f'Critical error: {err}')
  
finally:
    if 'dht' in locals():
        dht.deinit()
    if 'led' in locals(): 
        led.off()
        led.close()
    if 'client_sock' in locals():
        client_sock.close()
    if 'server_sock' in locals():
        server_sock.close()
    print('All resources cleaned up.')