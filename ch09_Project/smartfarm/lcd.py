# file: lcd.py

from time import sleep
from datetime import datetime
from RPLCD.i2c import CharLCD
from config import LCD_INTERVAL

lcd = CharLCD(i2c_expander='PCF8574', 
              address=0x27, 
              port=1,``
              cols=16, 
              rows=2, 
              charmap='A00')

# LCD 화면을 업데이트하는 함수 (main.py의 중앙 루프에서 호출됨)
def update_lcd_display(status):
    try:
        temp = status.get('temp')
        hum = status.get('hum')
        moisture = status.get('moisture')
        water_level = status.get('water_level')
        message = status.get('system_message', 'Initializing...')

        # 1. 온도/습도 표시
        temp_str = f'{temp:.1f}' if temp is not None else '---'
        hum_str = f'{hum:.1f}' if hum is not None else '---'
        
        lcd.clear()
        lcd.write_string(f'Temp : {temp_str} C\nHum  : {hum_str} %')
        sleep(LCD_INTERVAL) # 2초간 표시

        # 2. 토양/수위 표시
        moisture_str = f'{moisture:.1f}' if moisture is not None else '---'
        water_str = f'{water_level:.1f}' if water_level is not None else '---'

        lcd.clear()
        lcd.write_string(f'Moist : {moisture_str}\nWater : {water_str}')
        sleep(LCD_INTERVAL) # 2초간 표시

        # 3. 시스템 메시지 또는 시간 표시
        lcd.clear()
        lcd.write_string(f"{message}\n{datetime.now().strftime('%Y-%m-%d %H:%M')}")
        sleep(LCD_INTERVAL) # 2초간 표시

    except Exception as err:
        print(f'[LCD Error] {err}')

def lcd_cleanup():
    try:
        lcd.clear()
        lcd.backlight_enabled = False
        lcd.close()
        print('[LCD] Resource released.')
    except Exception:
        pass