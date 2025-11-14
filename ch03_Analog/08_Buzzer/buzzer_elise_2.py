# file: buzzer_elise_2.py

from gpiozero import TonalBuzzer
from gpiozero.tones import Tone
from time import sleep

bz = TonalBuzzer(13)

midi = [76, 75, 76, 75, 76, 71, 74, 72, 69, 60, 64, 69, 71, 64, 68, 71, 72]
interval = [0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 1, 0.5, 0.5, 0.5, 1, 0.5, 0.5, 0.5, 1]

print('Press Ctrl+C to exit')

for m, i in zip(midi, interval):
    bz.play(Tone(m))
    sleep(i)

bz.stop()
sleep(0.5)
