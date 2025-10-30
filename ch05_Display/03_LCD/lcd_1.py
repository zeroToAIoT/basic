# file: lcd_1.py

from time import sleep
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
    lcd.cursor_pos = (0, 0)         # set cursor position (row, column)
    lcd.write_string('ZERO TO AI !!')
    
    lcd.cursor_pos = (1, 0)         # set cursor position (row, column)
    lcd.write_string('PHYSICAL AI !!')
    
    sleep(2)
    
    lcd.clear()
    
    sleep(1)