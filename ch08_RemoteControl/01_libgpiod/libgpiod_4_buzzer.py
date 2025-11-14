# libgpiod_4_buzzer.py

from signal import pause
from gpiozero import MotionSensor, TonalBuzzer  
from gpiozero.pins.native import NativeFactory

remote_factory = NativeFactory(
    host='192.168.137.30',
    user='pi',
    password='12345678'
)

pir = MotionSensor(4, pin_factory=remote_factory)
bz = TonalBuzzer(13, pin_factory=remote_factory)

def motion_detected():
    print('Motion detected. Buzzer ON')
    bz.play(1000)       # 1000 Hz

def motion_not_detected():
    print('Motion not detected. Buzzer OFF')
    bz.stop()

pir.when_motion = motion_detected
pir.when_no_motion = motion_not_detected

print('Connecting to the Raspberry Pi...')
print('Press Ctrl+C to exit')
print('-'*30)

try:
    pause()

except Exception as err:
    print(f'Error : {err}')

finally:
    remote_factory.close()