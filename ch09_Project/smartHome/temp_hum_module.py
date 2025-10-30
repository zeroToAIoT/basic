# file: temp_hum_module.py
# Temperature and Humidity Sensor Module using DHT11

from adafruit_dht import DHT11
from config import PIN

dht = DHT11(PIN['TEMP_HUM'], use_pulseio=False)

def read_temp_hum():
    try:
        temp = dht.temperature
        hum = dht.humidity

        if temp is not None and hum is not None:
            print(f'Temperature : {temp:.1f}C, Humidity : {hum:.1f}%')
            return temp, hum
        else:
            print('Failed..data available.')
            return None, None
        
    except Exception as err:
        print(f'Error reading DHT sensor: {err}')
        return None, None
    
