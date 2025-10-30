# file: temp_hum.py
# Temperature and Humidity Sensor Module

from adafruit_dht import DHT11
from config import PIN

dht = DHT11(PIN['TEMP_HUM'], use_pulseio=False)

def read_temp_hum():
    try:
        temp = dht.temperature
        hum = dht.humidity

        if temp is None:
            print('[TempHum] Invalid temperature reading')
        if hum is None:
            print('[TempHum] Invalid humidity reading')

        return temp, hum

    except Exception as err:
        print(f'[TempHum Error] Sensor read error: {err}')
        return None, None