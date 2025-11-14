# file: config.py
# settings for the smart farm project

import board

# settings for GPIO pins
PIN = {
    'FAN': (5, 6),
    'SERVO': 23,
    'TEMP_HUM': board.D17,
    'RED': 25,
    'GREEN': 20,
    'BLUE': 21,
    'BUTTON': 4,
    'BUZZER': 18,
    'WATER_PUMP': (12, 16),
}

# settings for mcp3008 channels
MCP = {
    'LIGHT_SENSOR': 2,
    'WATER_SENSOR': 4,
    'MOISTURE_SENSOR': 7,
}

LCD_INTERVAL = 2
WATER_PUMP_INTERVAL = 5
WATER_TANK_INTERVAL = 5

# sensor thresholds
def get_threshold(sensor_type):
    thresholds = {
        'light': 0.3,
        'temp_high': 30,
        'temp_low': 20,
        'hum_high': 70,
        'hum_low': 40,
        'moisture_low': 0.4,
        'moisture_high': 0.8,
        'water_low': 0.3,
        'water_high': 0.8,
        'fire_high': 0.5,
    }
    return thresholds.get(sensor_type, None)

SENSOR_READ_INTERVAL = 10

# camera settings
CAMERA_RESOLUTION = (1280, 720)
CAMERA_FRAMERATE = 30
CAMERA_INTERVAL = 60*60*12   # 12 hours

# path
IMAGE_PATH = '/home/pi/smartfarm_venv/images/'
MUSIC_PATH = '/home/pi/smartfarm_venv/music/'
DB_PATH = '/home/pi/smartfarm_venv/DB/smartfarm.db'
MODEL_PATH = '/home/pi/smartfarm_venv/model/plant_growth.tflite'

GROWTH_LABELS = {
    1: 'Start 단계 (청색광)',
    2: 'Growth 단계 (보라광)',
    3: 'Flowering 단계 (적색광)',
    4: 'Fruition 단계 (주황광)'
}

# setting bluedot button (4 * 4 grid)
BLUEDOT_BUTTONS = {
    'activate': (0, 0),
    'deactivate': (0, 1),
    'fan_on': (0, 2),
    'fan_off': (0, 3),
    'water_pump_on': (1, 0),
    'water_pump_off': (1, 1),
    'waterTank_servo_on': (1, 2),
    'waterTank_servo_off': (1, 3),
    'rgb_white': (2, 0),
    'rgb_red': (2, 1),
    'rgb_blue': (2, 2),
    'rgb_off': (2, 3),
    'music_play': (3, 0),
    'music_stop': (3, 1),
}