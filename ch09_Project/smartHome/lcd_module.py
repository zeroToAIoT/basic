# file: lcd_module.py
# LCD Display Module

from time import sleep
import drivers
from temp_hum_module import read_temp_hum
from fire_module import fire_detect
from pir_module import read_pir_value

lcd = drivers.Lcd()

def lcd_blink(count):           # Blink the LCD backlight
    for _ in range(count):
        lcd.lcd_backlight(1)
        sleep(0.3)
        lcd.lcd_backlight(0)
        sleep(0.3)

    lcd.lcd_backlight(1)

def lcd_fire():           # Display fire alert
    lcd.lcd_clear()
    lcd_blink(3)
    lcd.lcd_display_string('!!! FIRE ALERT !!!', 1)
    lcd.lcd_display_string('Evacuate immediately!', 2)
    print('Fire detected! Emergency alert displayed.')

def lcd_pir_display(location):         # Display PIR alert
    lcd.lcd_clear()
    lcd_blink(2)

    if location == None:
        lcd.lcd_display_string('No motion detected', 1)
        lcd.lcd_display_string('ALL cleared!', 2)
    elif location == 'door':
        lcd.lcd_display_string('Motion at DOOR!', 1)
        lcd.lcd_display_string('Check DOOR!', 2)
    elif location == 'window':
        lcd.lcd_display_string('Motion at WINDOW!', 1)
        lcd.lcd_display_string('Check WINDOW!', 2)
    else:
        lcd.lcd_display_string('Error', 1)
        lcd.lcd_display_string('Check connections', 2)
        print('Error displaying PIR alert')

def lcd_temp_hum():        # Display temperature and humidity
    temp, hum = read_temp_hum()
    lcd.lcd_clear()
    if temp is not None and hum is not None:
        lcd.lcd_display_string(f'Temp: {temp:.1f}C', 1)
        lcd.lcd_display_string(f'Hum: {hum:.1f}%', 2)
        print(f'Displaying Temp: {temp:.1f}C, Hum: {hum:.1f}%')
    else:
        lcd.lcd_display_string('Sensor Error', 1)
        lcd.lcd_display_string('Check connections', 2)
        print('Failed to read sensor data.')

def lcd_display():      # Main loop for LCD display
    while True:
        try:
            fire_alert = fire_detect()
            pir_location = read_pir_value()

            if fire_alert:
                lcd_fire()
            elif pir_location:
                lcd_pir_display(pir_location)
                sleep(2)
                
                lcd_temp_hum() 
            else:
                lcd_temp_hum()
                
            sleep(1.5)

        except Exception as e:
            print(f'LCD Error: {e}')