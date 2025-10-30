# file: fan.py
# Activate the fan motor based on temperature and humidity values

from time import sleep
from gpiozero import Motor

from config import PIN, get_threshold, SENSOR_READ_INTERVAL
from temp_hum import read_temp_hum

# 팬 모터 핀 설정
fan = Motor(PIN['FAN'])

def control_fan(stop_event):
    """
    자동 팬 제어 루프
    stop_event가 set() 되면 루프 종료
    """
    try:
        while not stop_event.is_set():
            temp, hum = read_temp_hum()

            if temp is not None and hum is not None:
                if temp >= get_threshold('temp_high') or hum <= get_threshold('hum_low'):
                    print(f'[Fan] ON: Temp={temp:.1f}, Humidity={hum:.1f}')
                    fan.forward()
                else:
                    print(f'[Fan] OFF: Temp={temp:.1f}, Humidity={hum:.1f}')
                    fan.stop()
            else:
                print('[Fan] Failed to read sensor data. Fan OFF for safety.')
                fan.stop()

            # config.py에서 정의한 주기 사용
            for _ in range(SENSOR_READ_INTERVAL):
                if stop_event.is_set():
                    break
                sleep(1)

    except KeyboardInterrupt:
        fan.stop()
        print('[Fan] Control stopped. Ctrl+C.')
    except Exception as e:
        fan.stop()
        print(f'[Fan Error] {e}')


# Manual control functions for BlueDot
def fan_on():
    """Manually turn on the fan"""
    try:
        fan.forward()
        print('[Fan] Manually turned ON')
    except Exception as e:
        print(f'[Fan Error] turning on: {e}')


def fan_off():
    """Manually turn off the fan"""
    try:
        fan.stop()
        print('[Fan] Manually turned OFF')
    except Exception as e:
        print(f'[Fan Error] turning off: {e}')