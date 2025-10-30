# file: pigpio_4_buzzer.py
# refer : ch02_Basic/03_Buzzer/buzzer_2.py

from signal import pause
from gpiozero import MotionSensor, Buzzer
from gpiozero.pins.pigpio import PiGPIOFactory

ip = '192.168.137.161'          # Raspberry Pi IP address
remotePi = PiGPIOFactory(host=ip)

pir = MotionSensor(25, pin_factory=remotePi)
bz = Buzzer(13, pin_factory=remotePi)
   
def motion_detected():
    print('Motion detected. Buzzer ON')
    bz.on()

def motion_not_detected():
    print('Motion not detected. Buzzer OFF')
    bz.off()

pir.when_motion = motion_detected
pir.when_no_motion = motion_not_detected

print('Press Ctrl+C to exit')
print('-'*30)

try:
    pause()
        
except KeyboardInterrupt:
    print('Stopped by Ctrl+C.')
except Exception as err:
    print(f'Error : {err}')

finally:
    bz.close()        # Optional (includes bz.off())
    remotePi.close()    # Required!
    print('Finished.')