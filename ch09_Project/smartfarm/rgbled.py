# file: rgbled.py
# RGB LED Control Based on Light Sensor and Plant Growth Level

from gpiozero import RGBLED
from config import PIN, get_threshold

led = RGBLED(
    red=PIN['RED'],
    green=PIN['GREEN'],
    blue=PIN['BLUE']
)

def update_rgbled(light_value, growth_level, confidence=None):
    """Update RGB LED based on light sensor and plant growth level"""
    try:
        if growth_level is None:
            print('[RGBLED] Growth level not detected, keeping LED unchanged')
            return

        if confidence is not None and confidence < 0.6:
            print(f'[RGBLED] Low confidence ({confidence:.2f}), skipping update')
            return

        if light_value < get_threshold('light'):
            print('[RGBLED] Dark → Turning on RGB LED')
            set_color(growth_level)
        else:
            print('[RGBLED] Bright → Turning off RGB LED')
            led.off()

    except Exception as err:
        print(f'[RGBLED Error] {err}')


def set_color(color_input):
    try:
        if isinstance(color_input, str):
            # String color names for manual control
            color_map = {
                'white': (1, 1, 1),
                'red': (1, 0, 0),
                'blue': (0, 0, 1),
                'green': (0, 1, 0),
                'off': (0, 0, 0)
            }
            led.color = color_map.get(color_input.lower(), (0, 0, 0))  # Default: off
            print(f'[RGBLED] Set color to {color_input}')
        else:
            # Numeric growth level for automatic control
            colors = {
                1: (0, 0, 1),    # Blue (start)
                2: (1, 0, 1),    # Purple (growth)
                3: (1, 0, 0),    # Red (flowering)
                4: (1, 0.5, 0)   # Orange (fruition)
            }
            led.color = colors.get(color_input, (0, 0, 0))  # Default: off
            print(f'[RGBLED] Growth Level {color_input} → Color Updated')

    except Exception as err:
        print(f'[RGBLED Error] Setting color: {err}')