# file: pigpio_6_pir_lcd.py
# refer : ch05_Display/03_LCD/lcd_3.py

from signal import pause
from gpiozero import MotionSensor
from gpiozero.pins.pigpio import PiGPIOFactory
from RPLCD.i2c import CharLCD


ip = '192.168.137.162'          # Raspberry Pi IP address
remotePi = PiGPIOFactory(host=ip)

# 객체 생성 pir, lcd
pir = MotionSensor(25, pin_factory=remotePi)
lcd = CharLCD(i2c_expander='PCF8574', 
              address=0x27, 
              port=1,
              cols=16, 
              rows=2,
              charmap='A00')
lcd.clear()
lcd.backlight_enabled = True

def motion_detected():
    print('Motion detected')
    lcd.clear()
    lcd.backlight_enabled = True
    lcd.cursor_pos = (0, 0)
    lcd.write_string('Warning !!')
    lcd.cursor_pos = (1, 0)
    lcd.write_string('Motion detected')

def no_motion_detected():
    print('No motion detected')
    lcd.clear()
    lcd.backlight_enabled = False
    lcd.cursor_pos = (0, 0)
    lcd.write_string('All clear !!')
    lcd.cursor_pos = (1, 0)
    lcd.write_string('No motion detected')

pir.when_motion = motion_detected
pir.when_no_motion = no_motion_detected

try:
    pause()

except KeyboardInterrupt:
    print('Stopped. Ctrl+C pressed.')
except Exception as err:
    print(f'Error : {err}')

finally:
    pir.close()
    lcd.clear()
    lcd.close()
    remotePi.close()
    print('finished..')