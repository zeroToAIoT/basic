# file: lcd_3.py

from time import sleep
from datetime import datetime
from RPLCD.i2c import CharLCD

lcd = CharLCD(i2c_expander='PCF8574', 
              address=0x27, 
              port=1,
              cols=16, 
              rows=2,
              charmap='A00')

# initialize LCD
lcd.clear()
lcd.backlight_enabled = True # backlight on

print('Press Ctrl+C to exit')
print('-'*30)

while True:
    now = datetime.now()
    
    date_str = f'Date {now.strftime("%Y-%m-%d")}'
    
    time_str = f'Time {now.strftime("%H:%M:%S")}'
    
    lcd.cursor_pos = (0, 0)
    lcd.write_string(date_str)
    
    lcd.cursor_pos = (1, 0)
    lcd.write_string(time_str)
    
    sleep(1)