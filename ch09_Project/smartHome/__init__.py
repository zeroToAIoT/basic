# file: __init__.py

'''
SmartHome Package Initialization

스마트홈 프로젝트 파일 구조

원격 접속

1. main.py: 메인 로직, 각 기능별 모듈을 import하여 전체 시스템을 제어. 실행 파일.
2. config.py: GPIO 핀 번호, 센서 임계값, 환경변수 등 설정 정보를 관리
3. 각 기능 구현 파일 존재 (/home/pi/smartHome 디렉터리 내)
	__init__.py : 패키지 처리
 	1) 기본 환경 제어 기능
    led_module.py: LED 조명 제어 관련 기능을 담당.
    light_module.py: 조도 센서 관련 기능을 담당.

	2) 온습도 및 화재 감지 기능
    temp_hum_module.py: 온습도 센서 관련 기능을 담당.
    fire_module.py: 화재 감지 관련 기능을 담당.

	3) 디스플레이 기능
    multiFnd_module.py: 다중 FND 제어 관련 기능을 담당.
    lcd_module.py: LCD 제어 관련 기능을 담당.

	4) 보안 기능
	pir_module.py: PIR 센서 관련 기능을 담당.
    camera_module.py: 카메라 관련 기능을 담당.

 	5) 알람 기능
    buzzer_module.py: 부저 제어 관련 기능을 담당.
    morningCall_module.py: 아침 알람 기능을 담당.

	6) 시스템 활성화 / 비활성화
	button_module.py: 물리적 버튼 제어 관련 기능을 담당.
    bluedot_module.py: 블루투스 제어 관련 기능을 담당.
    
4. 디렉터리 구조
/home/pi/smartHome : 프로젝트 루트 디렉터리
/home/pi/smartHome/music : 음악 파일 저장
/home/pi/smartHome/capture : 캡처 이미지 파일 저장
/home/pi/smartHome/drivers : lcd driver
/home/pi/smartHome/logs : 로그 파일 저장

---------------------------------------------------------------------------------
5. 모듈 파일의 기능 구현 (/home/pi/smartHome 디렉터리 내)

	led_module.py
		def by_light():
		def by_fire(fire_detected):
		def by_pir(pir_detected):

	light_module.py
		def read_light_value():

	temp_hum_module.py
		def read_temp_hum():

	fire_module.py
		def fire_detect():
		def fire_detect():

	multiFnd_module.py
		def multiFnd_display_time():

	lcd_module.py
		def lcd_blink(count):
		def lcd_fire():
		def lcd_pir_display(location):
		def lcd_temp_hum():
		def lcd_display():

	pir_module.py
		def pir_detect():
	
	camera_module.py
		def capture_image(location):
		
	buzzer_module.py
		def by_fire(fire_detected):
		def by_pir(pir_detected):

	morningCall_module.py
		def morningCall_play():
        
	button_module.py
		def set_control_functions(activate, deactivate, get_status):
		def toggle_system():

	bluedot_module.py
		def set_control_functions(activate, deactivate):
		def activate():
		def deactivate():

	main.py
		def activate():
		def deactivate():
		def get_system_status():
		def main():

---------------------------------------------------------------------------------
'''