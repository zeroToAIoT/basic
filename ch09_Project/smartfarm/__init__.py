# file: __init__.py

'''
Smart Farm Project - 파일 구조
(스마트팜 시스템의 전체 디렉토리 및 파일 구성)

smartfarm/
│
├── __init__.py           # 이 파일. 패키지 초기화 및 프로젝트 구조 명세
├── config.py             # 시스템 환경 설정 (GPIO 핀, 임계값, 파일 경로 등)
│
├── main.py               # 스마트팜 메인 실행 파일. 중앙 허브 역할.
├── create_db.py          # SQLite 데이터베이스 초기 생성 스크립트 (최초 1회 실행).
│
├── server.py             # Flask 웹 서버 실행 파일. 데이터 시각화 및 원격 제어.
├── monitoring.html       # 웹 대시보드 템플릿.
│
├── light.py              # 조도 센서 데이터 읽기 모듈.
├── temp_hum.py           # DHT11 온습도 센서 데이터 읽기 모듈.
├── moisture.py           # 토양 습도 센서 데이터 읽기 모듈.
├── waterSensor.py        # 물탱크 수위 센서 데이터 읽기 모듈.
│
├── rgbled.py             # RGB LED 조명 제어 모듈.
├── fan.py                # DC 팬 모터 제어, 온도/습도 조절 모듈.
├── supplyWaterMoisture.py # 토양 습도 기반 물 펌프 제어, 물 공급 모듈.
├── supplyWaterTank.py    # 물탱크 수위 기반 서보 모터 밸브 제어, 물 보충 모듈.
├── buzzer.py             # 부저 제어, 알림 발생 모듈.
├── lcd.py                # I2C LCD 디스플레이 제어, 상태 정보 출력 모듈.
├── music.py              # 배경 음악 재생 및 제어 모듈.
│
├── button.py             # 물리 버튼 입력 처리 모듈.
├── bluedot.py            # BlueDot 앱을 통한 원격 제어 모듈.
│
├── camera.py             # 라즈베리 파이 카메라 제어, 주기적 이미지 캡처 모듈.
├── plantGrowth.py        # 캡처 이미지로 식물 성장 분석 및 DB 저장 모듈.
├── image_processing.py   # AI 모델 기반 이미지 전처리 및 식물 성장 추론 모듈.
├── train_model.py        # (PC/워크스테이션) AI 모델 학습 스크립트.
│
└── assets/               # 외부 파일 저장 루트 디렉터리
    ├── music/            # 배경 음악 MP3 파일 저장 디렉터리
    ├── images/           # 식물 성장 이미지 저장 디렉터리
    ├── db/               # SQLite 데이터베이스 파일 저장 디렉터리
    ├── model/            # 학습된 AI 추론 모델 저장 디렉터리
'''