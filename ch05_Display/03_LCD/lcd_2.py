# file: lcd_2.py

from time import sleep
from RPLCD.i2c import CharLCD

lcd = CharLCD(i2c_expander='PCF8574', 
              address=0x27, 
              port=1,
              cols=16, 
              rows=2,
              charmap='A00')

# initialize LCD
lcd.clear()
lcd.backlight_enabled = True # backlight on

print('Press Ctrl+C to exit')
print('-'*30)

message1 = 'Welcome to ZeroToAI !!'
message2 = 'Physical AI is coming !! '

# function to scroll both lines simultaneously
def scroll_both_lines(text1, text2, delay=0.3):
    # add spaces before and after text
    padded_text1 = ' ' * 16 + text1 + ' ' * 16
    padded_text2 = ' ' * 16 + text2 + ' ' * 16
    
    # scroll longer text
    max_length = max(len(padded_text1), len(padded_text2))
    
    for i in range(max_length - 15):
        lcd.clear()
        
        # display first line
        lcd.cursor_pos = (0, 0)
        if i < len(padded_text1) - 15:
            lcd.write_string(padded_text1[i:i+16])
        
        # display second line
        lcd.cursor_pos = (1, 0)
        if i < len(padded_text2) - 15:
            lcd.write_string(padded_text2[i:i+16])
        
        sleep(delay)

while True:
    scroll_both_lines(message1, message2, 0.3)
    sleep(1)