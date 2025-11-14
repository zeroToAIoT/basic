# file: lcd_7.py

import board, adafruit_dht
from RPLCD.i2c import CharLCD
from time import sleep

dht = adafruit_dht.DHT11(board.D21, use_pulseio=False)

lcd = CharLCD(i2c_expander='PCF8574', 
              address=0x27, 
              port=1,
              cols=16, 
              rows=2,
              charmap='A00')

lcd.clear()
lcd.backlight_enabled = True

print('Press Ctrl+C to exit')
print('-'*30)

while True:
    temp = dht.temperature
    hum = dht.humidity
    lcd.clear()

    if hum is not None and temp is not None:
        lcd.cursor_pos = (0, 0)
        lcd.write_string(f'Temp : {temp:.1f}C')
        lcd.cursor_pos = (1, 0)
        lcd.write_string(f'Hum  : {hum:.1f}%')
        print(f'Temperature : {temp:.1f}C, Humidity : {hum:.1f}%')
        print('-'*30)
        sleep(2)
    else:
        lcd.clear()
        lcd.cursor_pos = (0, 0)
        lcd.write_string('Failed to read sensor data.')
        print('Failed to read sensor data.')