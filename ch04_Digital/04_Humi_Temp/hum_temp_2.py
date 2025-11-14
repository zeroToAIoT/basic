# file: hum_temp_2.py

import board, adafruit_dht
from time import sleep

dht = adafruit_dht.DHT11(board.D21, use_pulseio=False)

def read_temperature():
    temp = dht.temperature
    print(f'Temperature: {temp:.1f}C')

def read_humidity():
    hum = dht.humidity
    print(f'Humidity: {hum:.1f}%')

print('Press Ctrl+C to exit')
print('-'*30)

while True:
    read_temperature()
    read_humidity()

    sleep(2)

