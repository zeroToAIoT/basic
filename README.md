# zeroToAI - BASIC

이 저장소는 『피지컬AI 컴퓨팅 - 센서편, 라즈베리파이와 파이썬으로 배우는 센서 제어와 스마트 프로젝트』의 기본 실습 코드(`basic`)를 포함하고 있습니다. 교재는 피지컬AI 입문자를 위한 실습 중심의 구성으로, Python과 센서 기반 프로젝트를 통해 AI의 핵심 개념을 직접 체험할 수 있도록 설계되었습니다.

## 📦 디렉터리 구조

### ch02_Basic - 기본 GPIO 제어
- **01_LED**: LED 기본 제어 (켜기/끄기, 깜빡이기)
- **02_Button**: 버튼 입력 처리
- **03_LED_Button**: LED와 버튼 결합 실습
- **04_PWMLED**: PWM을 이용한 LED 밝기 제어
- **05_TrafficLight**: 신호등 프로젝트
- **06_LEDBoard**: LED 보드 제어
- **07_LEDBarGraph**: LED 바그래프 제어
- **08_RGBLED**: RGB LED 제어

### ch03_Analog - 아날로그 센서
- **02_Potentiometer**: 가변저항(포텐셔미터) 제어
- **03_LightSensor**: 조도 센서 읽기
- **04_Temperature**: 온도 센서 읽기
- **05_water**: 물 센서 제어
- **06_sound**: 사운드 센서 제어
- **07_Joystick**: 조이스틱 입력 처리
- **08_Buzzer**: 부저 제어 및 멜로디 재생

### ch04_Digital - 디지털 센서
- **01_DistanceSensor**: 초음파 거리 센서
- **02_MotionSensor**: PIR 모션 센서
- **03_LineSensor**: 라인 트레이서 센서
- **04_Humi_Temp**: 온습도 센서 (DHT)

### ch05_Display - 디스플레이 출력
- **01_FND**: 7세그먼트 FND 제어
- **02_4digit_FND**: 4자리 FND 제어
- **03_LCD**: LCD 디스플레이 제어

### ch06_Actuator - 액추에이터 제어
- **02_servo**: 서보 모터 제어
- **04_DCmotor**: DC 모터 제어 및 속도 조절

### ch07_Camera - 카메라 제어
- 카메라 캡처, 스트리밍, 이미지 처리 실습

### ch08_RemoteControl - 원격 제어
- **01_pigpio**: pigpio를 이용한 원격 GPIO 제어
- **02_rfcomm**: 블루투스 RFCOMM 통신
- **03_bluedot**: BlueDot 앱을 이용한 스마트폰 제어

### ch09_Project - 통합 프로젝트
- **smartfarm**: 스마트팜 시스템 (식물 성장 모니터링, 자동 급수, AI 기반 성장 단계 인식)
- **smartHome**: 스마트홈 시스템 (LED, 센서, 부저, LCD 등 통합 제어)

### ch10_appendix - 부록
- 추가 예제 코드

## 🛠️ 설치 및 사용 방법

### 1. 저장소 클론
```bash
git clone https://github.com/zeroToAIoT/basic.git
cd basic
```

### 2. 필요한 패키지 설치
```bash
pip install -r requirements.txt
```

### 3. 라즈베리파이 설정
- 라즈베리파이 OS가 설치되어 있어야 합니다
- GPIO 핀 배선은 각 실습 예제에 따라 연결합니다

### 4. 실행
각 디렉터리의 Python 파일을 실행합니다:
```bash
python ch02_Basic/01_LED/led_1.py
```

## 📋 주요 의존성 패키지

- `gpiozero`: 라즈베리파이 GPIO 제어
- `RPLCD`: LCD 제어
- `adafruit-circuitpython-dht`: 온습도 센서
- `bluedot`: 스마트폰 원격 제어
- `picamera2`: 카메라 제어 (라즈베리파이 OS에 포함)
- `numpy`, `Pillow`: 이미지 처리
- `Flask`: 웹 서버 (프로젝트용)

## 📚 학습 경로

1. **기초**: ch02_Basic에서 LED, 버튼 등 기본 GPIO 제어 학습
2. **센서**: ch03_Analog, ch04_Digital에서 다양한 센서 활용
3. **출력**: ch05_Display에서 정보 표시 방법 학습
4. **구동**: ch06_Actuator에서 모터 제어 학습
5. **통합**: ch07_Camera, ch08_RemoteControl에서 고급 기능 학습
6. **프로젝트**: ch09_Project에서 실제 시스템 구축

## 📄 라이센스

이 프로젝트는 [MIT 라이센스](https://opensource.org/licenses/MIT)를 따릅니다.

## 🤝 기여

버그 리포트 및 기능 제안은 GitHub Issues를 이용해 주세요.
기능 추가나 개선 제안은 Fork 후 Pull Request를 보내주세요.
