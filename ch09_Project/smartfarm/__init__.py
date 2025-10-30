# file: __init__.py

'''
Smart Farm Project
스마트팜 프로젝트 파일 구조

smartfarm_venv/
│── __init__.py			#
│── config.py              # 환경 설정 (GPIO, 센서 임계값, 파일 경로 등)
│── light.py                  # 조도 센서 제어
│── temp_hum.py               # 온습도 센서 제어
│── moisture.py               # 토양 습도 센서 제어
│── waterSensor.py		# 물탱크 수위 센서 제어
│── rgbled.py                 # RGB LED 조명 제어
│── fan.py                    # 팬 모터 제어
│── supplyWaterMoisture.py	# 토양 물 공급 
│── supplyWaterTank.py		# 물탱크 물 공급 
│── buzzer.py			# 부저 제어
│── lcd.py                    # LCD 디스플레이 제어
│── music.py                  # 음악파일 및 연주 제어
│── button.py			# 버튼 제어
│── bluedot.py			# bluedot앱 원격 제어
│── camera.py			# 카메라 제어. 캡처
│── plantGrowth.py		# 식물 성장 모니터링 (사진 촬영)
│── image_processing.py	# 이미지 전처리 및 성장단계
│── train_model.py		# AI 학습
│── main.py			# 스마트팜 시스템 메인 실행 파일
│── create_db.py		# sqlite 생성(초기 1번만 실행)

│── server.py                  # flask server 제어
│── index.html			# 웹 대시보드(웹 브라우저에서 확인)

│── /                    	# 외부 파일 저장 디렉터리
│   ├── music/			# 음악 파일 저장 디렉터리
│   ├── images/          	# 식물 성장 이미지 저장 디렉터리
│   ├── db/          		# 데이터베이스 저장 디렉터리



'''