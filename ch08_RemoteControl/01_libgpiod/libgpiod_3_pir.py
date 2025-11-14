# libgpiod_3_pir.py

from signal import pause
from gpiozero import MotionSensor
from gpiozero.pins.native import NativeFactory

remote_factory = NativeFactory(
        host='192.168.137.30',
        user='pi',
        password='12345678'
    )

pir = MotionSensor(4, pin_factory=remote_factory)

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
    pir.close()         # Optional
    remote_factory.close()