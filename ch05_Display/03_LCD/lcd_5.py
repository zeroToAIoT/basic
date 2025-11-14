# file: lcd_5.py

from signal import pause
from gpiozero import MotionSensor
from RPLCD.i2c import CharLCD

pir = MotionSensor(25)

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

def motion_detected():
    print('Motion detected!')
    lcd.clear()
    lcd.cursor_pos = (0, 0)
    lcd.write_string('Warning !!')
    lcd.cursor_pos = (1, 0)
    lcd.write_string('Motion Detected !!')

def motion_stopped():
    print('Motion stopped')
    lcd.clear()
    lcd.cursor_pos = (0, 0)
    lcd.write_string('All clear !!')
    lcd.cursor_pos = (1, 0)
    lcd.write_string('No Motion !!')

pir.when_motion = motion_detected
pir.when_no_motion = motion_stopped

lcd.cursor_pos = (0, 0)
lcd.write_string('Motion Detector')
lcd.cursor_pos = (1, 0)
lcd.write_string('Ready !!')

pause()