# file: lcd_4.py

from time import sleep
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

while True:   
    if pir.motion_detected:
        print('Motion detected')
        lcd.write_string('Motion detected',(0, 0))
        lcd.write_string('Motion detected',(1, 0))
    else:
        print('No motion detected')
        lcd.write_string('No motion detected',(0, 0))
        lcd.write_string('No motion detected',(1, 0))
    
    sleep(0.5)
