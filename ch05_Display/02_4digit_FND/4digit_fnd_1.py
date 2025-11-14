# file: 4digit_fnd_1.py

from gpiozero import LEDCharDisplay, LEDMultiCharDisplay

display = LEDCharDisplay(20, 21, 19, 13, 6, 16, 12, dp=26)
multi_display = LEDMultiCharDisplay(display, 23, 24, 25, 5)

print('Press Ctrl+C to exit')

while True:
    multi_display.value = '8888'

'''
10~11행과 같은 기능을 함
# 한 번만 설정
multi_display.value = '8888'
pause()  # 무한 대기
'''
