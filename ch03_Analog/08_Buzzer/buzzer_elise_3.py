# file: buzzer_elise_3.py

from gpiozero import TonalBuzzer
from gpiozero.tones import Tone
from time import sleep

bz = TonalBuzzer(13)
speed = 0.3

midi = [76, 75, 76, 75, 76, 71, 74, 72, 69, 60, 64, 69, 71, 64, 68, 71, 72]
speedinterval = [speed, speed, speed, speed, speed, speed, speed, speed, speed+0.3, speed, speed, speed, speed+0.3, speed, speed, speed, speed+0.3]

print('Press Ctrl+C to exit')

while True:
    for m, i in zip(midi, speedinterval):
        bz.play(Tone(m))
        sleep(i)

    bz.stop()
    sleep(0.3)