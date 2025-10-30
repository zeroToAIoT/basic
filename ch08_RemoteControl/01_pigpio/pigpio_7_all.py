# file: pigpio_7_all.py
# refer : ch05_Display/03_LCD/lcd_3.py

from signal import pause
from datetime import datetime
import os
import drivers
from picamera2 import PiCamera2
from gpiozero import MotionSensor, Buzzer
from gpiozero.pins.pigpio import PiGPIOFactory

ip = '192.168.137.162'          # Raspberry Pi IP address
remotePi = PiGPIOFactory(host=ip)

save_dir = '/home/pi/starter/img'
os.makedirs(save_dir, exist_ok=True)

#create object - pir, cam, lcd
pir = MotionSensor(25, pin_factory=remotePi)
bz = Buzzer(13, pin_factory=remotePi)
lcd = drivers.Lcd()
cam = PiCamera2()

# configure camera
config = cam.create_still_configuration(main={'size': (1920, 1080)})
cam.configure(config)
cam.start()

def capture_image():
    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    filename = os.path.join(save_dir, f'{timestamp}.jpg')
    cam.capture_file(filename)
    print(f'Captured {filename}')

def motion_detected():
    print('Motion detected')
    capture_image()
    bz.on()
    lcd.lcd_clear()
    lcd.lcd_backlight(1)
    lcd.lcd_display_string('Warning !!', 1)
    lcd.lcd_display_string('Motion detected', 2)

def no_motion_detected():
    print('No motion detected')
    bz.off()
    lcd.lcd_clear()
    lcd.lcd_backlight(0)
    lcd.lcd_display_string('All clear !!', 1)
    lcd.lcd_display_string('No motion detected', 2)

pir.when_motion = motion_detected
pir.when_no_motion = no_motion_detected

print('Press Ctrl+C to exit')
print('-'*30)

# Check connection status
if remotePi.connected:
    print('Connected to the Raspberry Pi')
else:
    print('Not connected to the Raspberry Pi')

try:
    pause()

except KeyboardInterrupt:
    print('Stopped by Ctrl+C.')
except Exception as err:
    print(f'Error : {err}')

finally:
    pir.close()        # Optional
    bz.close()        # Optional
    lcd.lcd_clear()
    lcd.lcd_backlight(0)
    lcd.close()        # Optional
    cam.stop()         # Required!
    cam.close()        # Required!
    remotePi.close()    # Required!
    print('Finished.')