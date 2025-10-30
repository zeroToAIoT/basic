# file: RGBLED_5.py

from gpiozero import RGBLED
from time import sleep

rgbled = RGBLED(16, 20, 21)

color_map = {
    'black': (0, 0, 0),
    'white': (1, 1, 1),
    'red': (1, 0, 0),
    'orange': (1, 0.5, 0),
    'yellow': (1, 1, 0),
    'green': (0, 1, 0),
    'blue': (0, 0, 1),
    'navy': (0, 0, 0.5),
    'purple': (0.5, 0, 0.5),
    'lime': (0.5, 1, 0),
    'brown': (0.6, 0.3, 0),
    'gray': (0.5, 0.5, 0.5),
    'wine': (0.5, 0, 0),
    'skyblue': (0.678, 0.847, 0.902),
    'magenta': (0.5, 0, 0.5),
    'pink': (1, 0.75, 0.8)
}

# Function to set the color
def set_color(color_name):
    if color_name in color_map:
        rgbled.color = color_map[color_name]
        print(f'LED color set to {color_name}.')
    else:
        print(f'please enter a valid color name. {color_name} is an unknown color.')

# Function to show available colors
def show_available_colors():
    for name in color_map.keys():
        print(f'Color: {name}')

# Initial message
print('Enter a color name to set the LED. Type exit to quit.')
show_available_colors()  # Display available colors

print('Available colors:')

while True:
    # Get user input
    color_name = input('Enter color or type exit: ')
    if color_name.lower() == 'exit':  # Exit condition
        break
    set_color(color_name)

rgbled.off()  # Turn off LED
print('Program finished.')