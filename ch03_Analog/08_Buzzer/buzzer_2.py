# file: buzzer_2.py

from gpiozero import TonalBuzzer
from gpiozero.tones import Tone
from time import sleep

bz = TonalBuzzer(13)
sound = [60, 62, 64, 65, 67, 69, 71, 72]

print('Press Ctrl+C to exit')

while True:
    for s in sound:
        bz.play(Tone(s))
        print(f'{s} sound playing')
        sleep(0.5)

    bz.stop()
    sleep(1)