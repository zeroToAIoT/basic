# file: code_1.py               # code_1 모듈 파일

# 내장 라이브러리
from time import sleep            # time 라이브러리에서 sleep 함수 불러오기
from signal import pause          # signal 라이브러리에서 pause 함수 불러오기

# 외부 라이브러리
from gpiozero import LED           # gpiozero 라이브러리에서 LED 클래스 불러오기

led1 = LED(17)                     # LED 클래스로 led1 객체 생성
led2 = LED(27)                     # LED 클래스로 led2 객체 생성

count = 0                         # count 변수

print('Press Ctrl+C to exit')

def blink_led():                  # blink_led() 함수 정의
    led1.on()                       # led1 객체의 on 메서드 호출
    led2.on()                       # led2 객체의 on 메서드 호출
    sleep(1)                      # sleep() 함수 호출
    led1.off()                       # led1 객체의 off 메서드 호출
    led2.off()                       # led2 객체의 off 메서드 호출
    sleep(1)

print('Press Ctrl+C to exit')
print('-'*30)

led1.source = blink_led            # led1 객체의 source 속성에 blink_led 함수 할당
led2.source = blink_led            # led2 객체의 source 속성에 blink_led 함수 할당

pause()