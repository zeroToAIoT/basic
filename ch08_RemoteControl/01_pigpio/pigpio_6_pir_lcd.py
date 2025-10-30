# file: pigpio_6_pir_lcd.py
# refer : ch05_Display/03_LCD/lcd_3.py

from signal import pause
import drivers
from gpiozero import MotionSensor
from gpiozero.pins.pigpio import PiGPIOFactory


ip = '192.168.137.162'          # Raspberry Pi IP address
remotePi = PiGPIOFactory(host=ip)

#create object - pir, cam, lcd
pir = MotionSensor(25, pin_factory=remotePi)
lcd = drivers.Lcd()

def motion_detected():
    print('Motion detected')
    lcd.lcd_clear()
    lcd.lcd_backlight(1)
    lcd.lcd_display_string('Warning !!', 1)
    lcd.lcd_display_string('Motion detected', 2)

def no_motion_detected():
    print('No motion detected')
    lcd.lcd_clear()
    lcd.lcd_backlight(0)
    lcd.lcd_display_string('All clear !!', 1)
    lcd.lcd_display_string('No motion detected', 2)

pir.when_motion = motion_detected
pir.when_no_motion = no_motion_detected

print('Press Ctrl+C to exit')
print('-'*30)

try:
    pause()

except KeyboardInterrupt:
    print('Stopped. Ctrl+C pressed.')
except Exception as err:
    print(f'Error : {err}')

finally:
    pir.close()        # Optional
    lcd.lcd_clear()
    lcd.lcd_backlight(0)
    lcd.close()        # Optional
    remotePi.close()    # Required!
    print('Finished.')