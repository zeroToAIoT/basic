# file: hum_temp_4.py

import board, adafruit_dht
from gpiozero import LED
from time import sleep

dht = adafruit_dht.DHT11(board.D21, use_pulseio=False)
temp_red_led = LED(17)
hum_green_led = LED(27)

def check_temperature(temp):
    if temp is not None:
        if temp >= 30:
            print(f'Temperature: {temp:.1f}C, temp_red_led.on')
            temp_red_led.on()
        elif temp <= 15:
            print(f'Temperature: {temp:.1f}C, temp_red_led.off')
            temp_red_led.off()
        else:
            print(f'Temperature: {temp:.1f}C, temp_red_led.off')
            temp_red_led.off()
    else:
        print('No temperature data. Please check the sensor.')

def check_humidity(hum):
    if hum is not None:
        if hum >= 70:
            print(f'Humidity: {hum:.1f}%, hum_green_led.off')
            hum_green_led.off()
        elif hum <= 30:
            print(f'Humidity: {hum:.1f}%, hum_green_led.off')
            hum_green_led.off()
        else:
            print(f'Humidity: {hum:.1f}%, hum_green_led.on')
            hum_green_led.on()
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