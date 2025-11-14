# file: led_module.py
# led control module (Dumb Module)

from gpiozero import LED
from config import THRESHOLDS, PIN

led = LED(PIN['LED'])

# LED를 켜거나 끄는 기본 함수
def turn_on():
    led.on()
    print("LED ON.")

def turn_off():
    led.off()
    print("LED OFF.")

# LED를 깜빡이는 기본 함수
def blink_led(on_time, off_time, n=None):
    led.blink(on_time=on_time, off_time=off_time, n=n)
    print(f"LED blinking ({on_time}/{off_time}).")

# (기존 함수는 필요에 따라 더 명확하게 변경 가능)
# 예: by_light, by_fire, by_pir 함수 대신, 특정 목적의 함수로 변경
# 여기서는 기존 함수의 명칭은 유지하되, 인자를 받도록 수정했습니다.

def control_by_light(light_level): # 외부에서 light_level을 인자로 받음
    try:
        if light_level is None: # 인자가 유효한지 확인
            print("LED Control Error: Invalid light_level received.")
            return

        if light_level < THRESHOLDS['LIGHT_LOW']:
            print(f'Light level is {light_level:.2f}, Dark... Turning on LED.')
            led.on()
        elif light_level > THRESHOLDS['LIGHT_HIGH']:
            print(f'Light level is {light_level:.2f}, Bright.... Turning off LED.')
            led.off()
        else:
            print(f'Light level is {light_level:.2f}, Normal... Turning off LED.')
            led.off()
        
    except Exception as err:
        print(f'LED Control Error: {err}')
        led.off()

def control_by_fire(fire_detected): # 외부에서 fire_detected 값을 인자로 받음
    try:
        if fire_detected:
            print(f'Fire detected! Turning on LED (blink).')
            led.blink(on_time=0.2, off_time=0.2)
        else:
            print(f'No fire detected. Turning off LED.')
            led.off()
    except Exception as err:
        print(f'LED Control Error: {err}')
        led.off()

def control_by_pir(pir_detected): # 외부에서 pir_detected 값을 인자로 받음
    try:
        if pir_detected:
            print('Motion Detected.! Turning on LED (blink).')
            led.blink(on_time=0.5, off_time=0.5)
        else:
            print('No motion. Turning off LED.')
            led.off()
    except Exception as err:
        print(f'LED Control Error: {err}')
        led.off()

# 시스템이 비활성화될 때 LED를 끄는 함수 추가 (main에서 호출)
def cleanup():
    led.off()
    led.close()
    print("LED module cleaned up.")