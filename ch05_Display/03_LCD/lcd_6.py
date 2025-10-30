# file: lcd_6.py

from gpiozero import DistanceSensor
from RPLCD.i2c import CharLCD
from signal import pause

#ultra = DistanceSensor(echo=24, trigger=23)
ultra = DistanceSensor(24, 23, max_distance=1.0, threshold_distance=0.2)

lcd = CharLCD(i2c_expander='PCF8574', 
              address=0x27, 
              port=1,
              cols=16, 
              rows=2,
              charmap='A00')

lcd.clear()
lcd.backlight_enabled = True

def object_detected():
    lcd.clear()
    distance = ultra.distance
    lcd.cursor_pos = (0, 0)
    lcd.write_string('Object detected')
    lcd.cursor_pos = (1, 0)
    lcd.write_string(f'Distance: {distance:.2f}m')
    print(f'Distance: {distance:.2f}m')

def object_not_detected():
    lcd.clear()
    lcd.cursor_pos = (0, 0)
    lcd.write_string('No object detected')
    lcd.cursor_pos = (1, 0)
    lcd.write_string('No object detected')
    print('No object detected')

print('Press Ctrl+C to exit')
print('-'*30)

ultra.when_in_range = object_detected
ultra.when_out_of_range = object_not_detected

pause()