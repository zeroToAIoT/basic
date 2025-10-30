# file: pigpio_3_pir.py
# refer : ch02_Basic/02_MotionSensor/motion_2.py

from signal import pause
from gpiozero import MotionSensor
from gpiozero.pins.pigpio import PiGPIOFactory


ip = '192.168.137.161'          # Raspberry Pi IP address
remotePi = PiGPIOFactory(host=ip)

pir = MotionSensor(25, pin_factory=remotePi)

def motion_detected():
    print('Motion detected')

def no_motion_detected():
    print('No motion detected')

pir.when_motion = motion_detected
pir.when_no_motion = no_motion_detected

print('Press Ctrl+C to exit')
print('-'*30)

try:
    pause()

except KeyboardInterrupt:
    print('Stopped by Ctrl+C.')
except Exception as err:
    print(f'Error : {err}')

finally:
    pir.close()        # Optional
    remotePi.close()    # Required!
    print('Finished.')