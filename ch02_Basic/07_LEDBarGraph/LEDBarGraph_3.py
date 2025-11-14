# file: LEDBarGraph_3.py

from gpiozero import LEDBarGraph
from time import sleep

ledBar = LEDBarGraph(17, 27, 22, 13, 19)
DELAY = 0.5

print('Press Ctrl+C to exit')

while True:
    # Incremental brightness (0 ~ 5)
    for i in range(6):
        ledBar.value = i / 5
        print(f'LEDBarGraph value {i}/5')
        sleep(DELAY)
        
    # Decremental brightness (5 ~ 0)
    for i in range(5, -1, -1):
        ledBar.value = i / 5
        print(f'LEDBarGraph value set to {i}/5')
        sleep(DELAY)