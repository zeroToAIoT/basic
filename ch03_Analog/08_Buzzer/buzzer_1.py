# file: buzzer_1.py

from gpiozero import TonalBuzzer
from time import sleep

bz = TonalBuzzer(7)

sound = ['C4', 'D4', 'E4', 'F4', 'G4', 'A4', 'B4', 'C5']

print('Press Ctrl+C to exit')

while True:
    for s in sound:
        bz.play(s)
        print(f'{s} sound playing')
        sleep(1)

    bz.stop()
    sleep(0.1)