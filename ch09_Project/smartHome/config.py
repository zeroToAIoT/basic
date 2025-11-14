# file: config.py
# smartHome configuration file

import os
import board

# Raspberry Pi IP
REMOTE_PI_IP = os.getenv('REMOTE_PI_IP', '192.168.137.162')

# settings for GPIO pins
PIN = {
    'LED': 7,
    'BUZZER': 18,
    'BUTTON': 4,
    'PIR_DOOR': 27,
    'PIR_WINDOW': 22,
    'TEMP_HUM': board.D17,
}

# settings for MCP3008 channels
MCP3008_CHANNEL = {
    'FIRE_SENSOR': 0,
    'LIGHT_SENSOR': 2,
}

# settings for thresholds
THRESHOLDS = {
    'TEMP_HIGH': 30,    # temperature upper limit, degree C
    'TEMP_LOW': 18,     # temperature lower limit, degree C
    'HUM_HIGH': 60,     # humidity upper limit, %
    'HUM_LOW': 30,      # humidity lower limit, %
    'LIGHT_HIGH': 0.7,   # light upper limit, lux
    'LIGHT_LOW': 0.3,    # light lower limit, lux
    'FIRE_LOW': 0.2,     # fire lower limit, lux
    'FIRE_HIGH': 0.5,    # fire upper limit, lux
}

# Morning call music file path
# 상대 경로 사용: config.py가 있는 디렉토리를 기준으로 설정
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# 환경 변수가 설정되어 있으면 우선 사용 (원격 실행 시 유용)
BASE_DIR = os.getenv('SMARTHOME_BASE_DIR', BASE_DIR)

MUSIC_DIR = os.path.join(BASE_DIR, 'music')
LOG_PATH = os.path.join(BASE_DIR, 'logs')
