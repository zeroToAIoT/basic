# file: pigpio_5_melody.py
# refer : ch02_Basic/03_Buzzer/buzzer_2.py

from signal import pause
from time import sleep
from gpiozero import MotionSensor, TonalBuzzer
from gpiozero.pins.pigpio import PiGPIOFactory

ip = '192.168.137.30'          # Raspberry Pi IP address
remotePi = PiGPIOFactory(host=ip)

pir = MotionSensor(25, pin_factory=remotePi)
bz = TonalBuzzer(13, pin_factory=remotePi)

melody_O_Fortuna = [
    (440, 0.5), (440, 0.5), (440, 0.5), (349.23, 0.5), (523.25, 0.5),
    (440, 0.5), (349.23, 0.5), (523.25, 0.5), (440, 1.0), (659.26, 0.5),
    (659.26, 0.5), (659.26, 0.5), (698.46, 0.5), (698.46, 0.5), (698.46, 0.5),
    (659.26, 0.5), (659.26, 0.5), (659.26, 0.5), (698.46, 0.5), (523.25, 0.5),
    (523.25, 0.5), (523.25, 0.5), (440, 0.5), (349.23, 0.5), (523.25, 0.5),
    (440, 0.5), (349.23, 0.5), (523.25, 0.5), (440, 1.5), (659.26, 0.5),
    (440, 0.5), (523.25, 0.5), (523.25, 0.5), (440, 0.5), (349.23, 0.5),
    (523.25, 0.5), (440, 0.5), (349.23, 0.5), (523.25, 0.5), (440, 2.0)
]

def play_melody(melody):
    for freg, duration in melody:
        bz.play(freg)
        sleep(duration)
        bz.stop()
        sleep(0.05)

def motion_detected():
    print('Motion detected. Playing melody')
    play_melody(melody_O_Fortuna)

def motion_not_detected():
    print('Motion not detected. Stopping melody')
    bz.stop()

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
    bz.close()        # Optional (includes bz.stop())
    remotePi.close()    # Required!
    print('Finished.')