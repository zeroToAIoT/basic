# file: lcd_module.py
# LCD Display Module (Dumb Module) using RPLCD Library

from time import sleep
from RPLCD.i2c import CharLCD 

lcd = CharLCD(i2c_expander='PCF8574', address=0x27, port=1, 
              cols=16, rows=2, dotsize=8, 
              charmap='A00', 
              auto_linebreaks=True)

def set_backlight(on=True):
    lcd.backlight_enabled = on
    
def lcd_blink(count):           # Blink the LCD backlight
    for _ in range(count):
        set_backlight(True)
        sleep(0.3)
        set_backlight(False)
        sleep(0.3)
    set_backlight(True) 

def display_fire_alert():           # Display fire alert
    lcd.clear()
    lcd_blink(3)
    lcd.write_string('!!! FIRE ALERT !!!\nEvacuate immediately!') 
    print('LCD: Fire detected! Emergency alert displayed.')
  
def display_pir_alert(location):         # Display PIR alert
    lcd.clear()
    lcd_blink(2)
  
    if location == 'door':
        lcd.write_string('Motion at DOOR!\nCheck DOOR!')
    elif location == 'window':
        lcd.write_string('Motion at WINDOW!\nCheck WINDOW!')
    else: 
        lcd.write_string('No motion detected\nALL cleared!')
        print('LCD: No motion or invalid PIR location.')

def display_temp_hum(temp, hum):        # Display temperature and humidity
    lcd.clear()
    if temp is not None and hum is not None:
        lcd.write_string(f'Temp: {temp:.1f}C\nHum: {hum:.1f}%') 
        print(f'LCD: Displaying Temp: {temp:.1f}C, Hum: {hum:.1f}%')
    else:
        lcd.write_string('Sensor Error\nCheck DHT!')
        print('LCD: Failed to read DHT sensor data for display.')

def update_display(current_status):
    """
    LCD 디스플레이를 업데이트하는 메인 함수.
    current_status 딕셔너리에서 모든 필요한 정보를 받습니다.
    예: {'fire_alert': True, 'pir_location': 'door', 'temp': 25.0, 'hum': 50.0}
    """
    try:
        fire_alert = current_status.get('fire_alert', False)
        pir_location = current_status.get('pir_location', None)
        temp = current_status.get('temp', None)
        hum = current_status.get('hum', None)

        if fire_alert:
            display_fire_alert()
        elif pir_location:
            display_pir_alert(pir_location)
            sleep(2) 
        else:
            display_temp_hum(temp, hum)
        
    except Exception as err:
        print(f'LCD Update Error: {err}')
        lcd.clear()
        lcd.write_string('LCD SYSTEM ERROR\nCheck Console')

def cleanup():
    lcd.clear()
    set_backlight(False) 
    print("LCD module cleaned up.")
