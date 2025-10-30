# file: buzzer_elise_1.py

from gpiozero import TonalBuzzer
from time import sleep

bz = TonalBuzzer(13)

sound = ['E5', 'D#5', 'E5', 'D#5', 'E5', 'B4', 'D5', 'C5', 'A4','C4', 'E4', 'A4', 'B4', 'E4', 'G#4', 'B4', 'C5']
interval = [0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 1, 0.5, 0.5, 0.5, 1, 0.5, 0.5, 0.5, 1]

print('Press Ctrl+C to exit')

for s, i in zip(sound, interval):
    bz.play(s)
    sleep(i)

bz.stop()
sleep(0.5)
