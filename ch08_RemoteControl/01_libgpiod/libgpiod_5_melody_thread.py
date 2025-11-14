# file: libgpiod_5_melody_thread.py
  
from signal import pause
from time import sleep
from gpiozero import MotionSensor, TonalBuzzer
from gpiozero.pins.native import NativeFactory
from threading import Thread  # 1. 스레드 임포트
  
remote_factory = NativeFactory(
    host='192.168.137.30',
    user='pi',
    password='12345678'
)
  
pir = MotionSensor(4, pin_factory=remote_factory)
bz = TonalBuzzer(13, pin_factory=remote_factory)

# 2. 멜로디가 재생 중인지 상태를 저장할 플래그(깃발)
is_playing = False
  
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
    global is_playing
    is_playing = True  # "재생 시작" 플래그 올림
    print('Thread: 멜로디 재생 시작...')

    for freg, duration in melody:
        # 3. 매 순간 깃발을 확인해서, "멈춤" 신호가 오면 즉시 루프 탈출
        if not is_playing:
            print('Thread: 멜로디 중지 신호 받음.')
            break
            
        bz.play(freg)
        sleep(duration)
        bz.stop()
        
        # (긴 음표의 경우 sleep 중간에 멈출 수 없으므로, sleep 이후에도 확인)
        if not is_playing:
            print('Thread: 멜로디 중지 신호 받음 (sleep 후).')
            break
            
        sleep(0.05)
    
    print('Thread: 멜로디 재생 완료.')
    is_playing = False # "재생 끝" 플래그 내림
    bz.stop() # 혹시 모르니 한번 더 정지
  
def motion_detected():
    global is_playing
    # 4. 이미 재생 중이면, 또 실행하지 않음 (중복 방지)
    if is_playing:
        print('Motion detected (멜로디 재생 중, 무시)')
        return
        
    print('Motion detected. 멜로디 스레드 시작')
    # 5. 멜로디 재생을 별도 스레드로 분리해서 시작 (daemon=True)
    #    이렇게 하면 이 함수는 0.01초 만에 즉시 종료됨 (차단 안 함)
    t = Thread(target=play_melody, args=(melody_O_Fortuna,), daemon=True)
    t.start()
  
def motion_not_detected():
    global is_playing
    if is_playing:
        print('Motion not detected. 멜로디 중지 신호 전송')
        # 6. 플래그를 내려서 스레드에게 "멈추라"고 신호 보냄
        is_playing = False
        bz.stop() # 현재 울리는 음을 즉시 멈춤
    else:
        print('Motion not detected. (이미 멈춰있음)')
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
    is_playing = False # 프로그램 종료 시 스레드 정지
    bz.stop()
    remote_factory.close()
    print('Finished.')