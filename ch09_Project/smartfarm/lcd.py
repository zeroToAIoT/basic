# file: lcd.py
# LCD Display Module for Smart Farm Monitoring System

from time import sleep
from datetime import datetime
from RPLCD import CharLCD

from config import LCD_INTERVAL
from temp_hum import read_temp_hum
from moisture import read_moisture
from waterSensor import read_water_level

# RPLCD 설정 (16x2 LCD)
lcd = CharLCD(cols=16, rows=2, pin_rs=26, pin_e=19, pins_data=[13, 6, 5, 11], numbering_mode=1)


def display_lcd(stop_event):
    try:
        while not stop_event.is_set():
            temp, hum = read_temp_hum()
            moisture = read_moisture()
            water_level = read_water_level()

            temp_str = f'{temp:.1f}' if temp is not None else '---'
            hum_str = f'{hum:.1f}' if hum is not None else '---'
            moisture_str = f'{moisture:.1f}' if moisture is not None else '---'
            water_str = f'{water_level:.1f}' if water_level is not None else '---'

            now = datetime.now()
            lcd.clear()
            lcd.cursor_pos = (0, 0)
            lcd.write_string(now.strftime('%Y-%m-%d'))
            lcd.cursor_pos = (1, 0)
            lcd.write_string(now.strftime('%H:%M:%S'))
            for _ in range(LCD_INTERVAL):
                if stop_event.is_set():
                    break
                sleep(1)

            lcd.clear()
            lcd.cursor_pos = (0, 0)
            lcd.write_string(f'Temp : {temp_str} C')
            lcd.cursor_pos = (1, 0)
            lcd.write_string(f'Hum  : {hum_str} %')
            for _ in range(LCD_INTERVAL):
                if stop_event.is_set():
                    break
                sleep(1)

            lcd.clear()
            lcd.cursor_pos = (0, 0)
            lcd.write_string(f'Moist : {moisture_str}')
            lcd.cursor_pos = (1, 0)
            lcd.write_string(f'Water : {water_str}')
            for _ in range(LCD_INTERVAL):
                if stop_event.is_set():
                    break
                sleep(1)

    except KeyboardInterrupt:
        print('[LCD] Display stopped. Ctrl+C.')
    except Exception as err:
        print(f'[LCD Error] {err}')
    finally:
        try:
            lcd.close(clear=True)
            print('[LCD] Resource released.')
        except Exception:
            pass