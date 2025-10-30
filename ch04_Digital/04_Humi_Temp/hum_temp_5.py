# file: Hum_Temp_3.py

import board, adafruit_dht
from gpiozero import LED
from signal import pause
from time import sleep

dht = adafruit_dht.DHT11(board.D21, use_pulseio=False)
led_temp = LED(17)
led_hum = LED(27)

interval = 2

def check_temp():
    while True:
        temp = dht.temperature
        if temp is not None:
            print(f'Temperature: {temp:.1f}C')
            yield 1 if temp >= 30 else 0
        else:
            yield 0
        sleep(interval)

def check_hum():
    while True:
        hum = dht.humidity
        if hum is not None:
            print(f'Humidity: {hum:.1f}%')
            yield 1 if hum <= 30 else 0
        else:
            yield 0
        sleep(interval)

led_temp.source = check_temp()
led_hum.source = check_hum()

print('Press Ctrl+C to exit')
print('-'*30)

pause()