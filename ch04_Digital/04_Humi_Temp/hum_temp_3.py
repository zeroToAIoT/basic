# file: hum_temp_3.py

import board, adafruit_dht
from time import sleep

dht = adafruit_dht.DHT11(board.D21, use_pulseio=False)

def check_temperature(temp):
    if temp is not None:
        if temp >= 30:
            print(f'Temperature: {temp:.1f}C, Temperature is high.')
        elif temp <= 15:
            print(f'Temperature: {temp:.1f}C, Temperature is low.')
        else:
            print(f'Temperature: {temp:.1f}C, Temperature is optimal.')
    else:
        print('No temperature data. Please check the sensor.')

def check_humidity(hum):
    if hum is not None:
        if hum >= 70:
            print(f'Humidity: {hum:.1f}%, Humidity is high.')
        elif hum <= 30:
            print(f'Humidity: {hum:.1f}%, Humidity is low.')
        else:
            print(f'Humidity: {hum:.1f}%, Humidity is optimal.')
    else:
        print('No humidity data. Please check the sensor.')

print('Press Ctrl+C to exit')
print('-'*30)

while True:
    temp = dht.temperature
    hum = dht.humidity

    check_temperature(temp)
    check_humidity(hum)

    print('-'*30)

    sleep(2)