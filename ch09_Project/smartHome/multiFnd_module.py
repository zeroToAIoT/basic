# file: multiFnd_module.py
# dispay time on a 7-segment LED display

from gpiozero import LEDCharDisplay, LEDMultiCharDisplay
from time import sleep
from datetime import datetime
from system_status import is_system_active

char = LEDCharDisplay(20, 21, 19, 13, 6, 16, 12, dp=26)
display = LEDMultiCharDisplay(char, 23, 24, 25, 5)

def multiFnd_display_time():
    while is_system_active():
        try:
            now = datetime.now()
            current_time = now.strftime('%H:%M')
            display.value = current_time
            print(f'Now time: {current_time}')
            sleep(0.5)
        except Exception as err:
            print(f'Error : {err}')
    print("FND display stopped.")

def cleanup():
    """리소스 정리 함수"""
    global char, display
    try:
        if display:
            display.value = ""
            display.close()
        if char:
            char.close()
        print("FND module cleaned up.")
    except Exception as e:
        print(f"FND module cleanup error: {e}")