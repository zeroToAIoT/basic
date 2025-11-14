# SmartHome 프로젝트 연동성 상세 검토 보고서

## 📋 검토 개요
- **검토 일자**: 2024
- **검토 범위**: smartHome 프로젝트 전체 모듈 간 연동성
- **검토 목적**: 모듈 간 통신, 상태 공유, 의존성 관리, 스레드 안전성 확인

---

## 🔴 심각한 연동성 이슈

### 1. **이중 제어 문제: fire_module과 main.py의 충돌**

**위치**: 
- `fire_module.py` 33-34, 40-41번째 줄
- `main.py` 145-146번째 줄

**문제 상세**:
```python
# fire_module.py에서
led_module.control_by_fire(True)  # 직접 제어
buzzer_module.control_by_fire(True)  # 직접 제어

# main.py의 _monitor_and_control_loop()에서도
control_by_fire(True)  # 동시에 제어
```

**영향도**: 🔴 **매우 높음**
- 두 곳에서 동시에 LED와 부저를 제어하여 충돌 가능
- `fire_module.py`의 `monitor_fire_sensor()`가 2초마다 실행
- `main.py`의 `_monitor_and_control_loop()`가 1.5초마다 실행
- 타이밍에 따라 서로 덮어쓰는 문제 발생 가능

**현재 동작 흐름**:
1. `fire_module.monitor_fire_sensor()` 스레드가 화재 감지 시 LED/부저 직접 제어
2. `main.py._monitor_and_control_loop()` 스레드가 `get_current_fire_status()`로 상태 확인 후 LED/부저 제어
3. 두 스레드가 거의 동시에 같은 하드웨어를 제어하려고 시도

**권장 수정 방안**:
```python
# Option 1: fire_module은 상태만 감지 (권장)
# fire_module.py에서 LED/부저 제어 코드 제거
# main.py에서만 제어

# Option 2: 명확한 우선순위 설정
# fire_module의 제어를 우선시하고, main.py는 fire_module이 제어하지 않을 때만 제어
```

---

### 2. **cleanup 함수 누락 문제**

**위치**: 여러 모듈

**문제 상세**:
`main.py`에서 다음 모듈들의 cleanup을 호출하지만, 실제로 함수가 정의되어 있지 않음:

| 모듈 | cleanup 호출 여부 | cleanup 정의 여부 | 상태 |
|------|------------------|-------------------|------|
| `pir_module` | ✅ (pir_cleanup) | ❌ | **누락** |
| `fire_module` | ✅ (fire_cleanup) | ❌ | **누락** |
| `light_module` | ✅ (light_cleanup) | ❌ | **누락** |
| `temp_hum_module` | ✅ (dht_cleanup) | ❌ | **누락** |
| `camera_module` | ❌ | ❌ | **누락** |
| `bluedot_module` | ✅ (bluedot_cleanup) | ❌ | **누락** |
| `multiFnd_module` | ✅ (fnd_cleanup) | ❌ | **누락** |
| `morningCall_module` | ✅ (mc_cleanup) | ❌ | **누락** |

**영향도**: 🟠 **중간**
- 시스템 종료 시 리소스가 제대로 해제되지 않을 수 있음
- GPIO 핀, 센서, 카메라 등이 정상적으로 해제되지 않을 수 있음

**수정 필요**:
각 모듈에 cleanup 함수 추가:
```python
# 예시: pir_module.py
def cleanup():
    global pir_door, pir_window
    if pir_door:
        pir_door.close()
    if pir_window:
        pir_window.close()
    print("PIR module cleaned up.")
```

---

### 3. **순환 import 위험: button_module_advanced.py**

**위치**: `button_module_advanced.py` 9번째 줄

**문제 상세**:
```python
# button_module_advanced.py
from main import activate, deactivate

# main.py
from button_module import ...
```

**영향도**: 🟡 **낮음** (현재는 사용되지 않는 것으로 보임)
- `button_module_advanced.py`가 실제로 사용되지 않는다면 문제 없음
- 하지만 사용 시 순환 import로 인한 ImportError 발생 가능

**권장 사항**:
- 사용하지 않는다면 파일 삭제 또는 명확한 주석 추가
- 사용한다면 콜백 패턴으로 변경 (현재 `button_module.py`처럼)

---

### 4. **스레드 안전성 문제: 전역 변수 접근**

**위치**: 모든 센서 모듈

**문제 상세**:
각 모듈에서 전역 변수로 상태를 관리하지만 Lock이 없음:

| 모듈 | 전역 변수 | 접근하는 스레드 |
|------|----------|----------------|
| `pir_module.py` | `_motion_detected_at` | monitor_pir_sensors, main.py |
| `fire_module.py` | `_fire_alert_active` | monitor_fire_sensor, main.py |
| `light_module.py` | `_current_light_value` | monitor_light_sensor, main.py |
| `temp_hum_module.py` | `_current_temperature`, `_current_humidity` | monitor_temp_hum_sensor, main.py |

**영향도**: 🟡 **중간**
- 대부분의 경우 읽기 전용 접근이지만, 동시 쓰기 시 데이터 일관성 문제 가능
- `main.py`의 `_system_status`만 Lock이 있음

**권장 수정**:
```python
# 각 모듈에 threading.Lock 추가
import threading
_status_lock = threading.Lock()

def get_current_fire_status():
    with _status_lock:
        return _fire_alert_active
```

---

## 🟡 개선 권장 사항

### 5. **모듈 간 의존성 구조**

**현재 구조**:
```
fire_module.py → led_module.py, buzzer_module.py (직접 import)
pir_module.py → camera_module.py (직접 import)
main.py → 모든 모듈 (중앙 제어)
```

**권장 구조**:
- **센서 모듈**: 상태만 감지하고 반환
- **제어 모듈**: main.py에서만 하드웨어 제어
- **의존성 방향**: 센서 → main → 액추에이터 (단방향)

---

### 6. **에러 처리 및 복구 메커니즘**

**현재 상태**:
- 모니터링 루프에서 예외 발생 시 `sleep(5)` 후 재시도
- 하지만 시스템 상태(`is_system_active()`) 확인 없이 무한 재시도

**개선 방안**:
```python
def monitor_fire_sensor():
    error_count = 0
    max_errors = 5
    
    while is_system_active():
        try:
            fire_detect()
            error_count = 0  # 성공 시 리셋
            sleep(2)
        except Exception as e:
            error_count += 1
            print(f"Fire Monitoring Error ({error_count}/{max_errors}): {e}")
            
            if error_count >= max_errors:
                print("Fire sensor disabled due to repeated errors.")
                break  # 심각한 오류 시 해당 모듈만 비활성화
            
            sleep(5)
```

---

### 7. **config.py 경로 하드코딩**

**위치**: `config.py` 39번째 줄

**문제**:
```python
BASE_DIR = '/home/pi/smartHome'  # 절대 경로 하드코딩
```

**권장 수정**:
```python
import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# 또는
BASE_DIR = os.getenv('SMARTHOME_BASE_DIR', os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
```

---

### 8. **bluedot_module.py의 pause() 호출 위치**

**현재 구조**:
- `main.py`의 `_start_bluedot_service()`에서 `pause()` 호출
- 하지만 `bluedot_module.py`에서 이미 `bd` 객체가 생성되고 이벤트 핸들러가 설정됨

**검토 필요**:
- `pause()`가 별도 스레드에서 호출되는 것이 적절한지 확인
- BlueDot의 이벤트 처리가 메인 스레드에서 이루어져야 하는지 확인

---

## ✅ 잘 구현된 부분

1. **system_status.py 모듈**: 시스템 활성 상태를 중앙에서 관리
2. **모니터링 루프 구조**: 모든 센서 모니터링이 `is_system_active()` 체크
3. **함수 기반 인터페이스**: 모듈 간 통신이 함수 호출로 명확
4. **스레드 기반 아키텍처**: 동시성 처리를 위한 구조
5. **config.py 중앙 관리**: GPIO 핀, 임계값 등이 한 곳에서 관리

---

## 🔧 우선순위별 수정 권장사항

### 즉시 수정 필요 (P0)
1. ✅ **이중 제어 문제 해결**: `fire_module.py`에서 LED/부저 직접 제어 제거
2. ✅ **cleanup 함수 추가**: 모든 모듈에 cleanup 함수 구현
3. ✅ **순환 import 확인**: `button_module_advanced.py` 사용 여부 확인 및 수정

### 단기 개선 (P1)
4. ✅ **스레드 안전성 강화**: 전역 변수 접근에 Lock 추가
5. ✅ **config.py 경로 개선**: 상대 경로 또는 환경 변수 사용
6. ✅ **에러 처리 강화**: 센서별 독립적인 에러 카운터 및 복구 로직

### 중기 개선 (P2)
7. ✅ **모듈 간 의존성 구조 개선**: 명확한 계층 구조 정의
8. ✅ **테스트 코드 추가**: 모듈 간 연동 테스트
9. ✅ **로깅 시스템 도입**: print 대신 logging 모듈 사용

---

## 📊 모듈 간 연동 흐름도

### 현재 구조 (문제점 포함)
```
┌─────────────────┐
│   main.py       │
│  (중앙 제어)     │
└────────┬────────┘
         │
    ┌────┴────┬──────────┬──────────┐
    │         │          │          │
┌───▼───┐ ┌──▼───┐  ┌───▼───┐  ┌───▼───┐
│fire_  │ │pir_  │  │light_ │  │temp_  │
│module │ │module│  │module │  │hum_   │
└───┬───┘ └──┬───┘  └───┬───┘  └───┬───┘
    │        │          │          │
    │        │          │          │
    │   ┌────▼────┐     │          │
    │   │camera_  │     │          │
    │   │module   │     │          │
    │   └─────────┘     │          │
    │                   │          │
    │        ┌──────────┴──────────┘
    │        │
    │   ┌────▼────┐  ┌──────────┐
    └───►led_     │  │buzzer_   │
         │module  │  │module    │
         └────────┘  └──────────┘
         ▲
         │ (이중 제어 문제!)
         │
    ┌────┴────┐
    │main.py  │
    │제어 루프│
    └─────────┘
```

### 권장 구조
```
┌─────────────────┐
│   main.py       │
│  (중앙 제어)     │
└────────┬────────┘
         │
    ┌────┴────┬──────────┬──────────┐
    │         │          │          │
┌───▼───┐ ┌──▼───┐  ┌───▼───┐  ┌───▼───┐
│fire_  │ │pir_  │  │light_ │  │temp_  │
│module │ │module│  │module │  │hum_   │
│(상태) │ │(상태)│  │(상태) │  │(상태) │
└───┬───┘ └──┬───┘  └───┬───┘  └───┬───┘
    │        │          │          │
    │        │          │          │
    │   ┌────▼────┐     │          │
    │   │camera_  │     │          │
    │   │module   │     │          │
    │   └─────────┘     │          │
    │                   │          │
    │        ┌──────────┴──────────┘
    │        │
    │   ┌────▼────┐  ┌──────────┐
    └───►led_     │  │buzzer_   │
         │module  │  │module    │
         └────────┘  └──────────┘
         ▲
         │ (단일 제어)
         │
    ┌────┴────┐
    │main.py  │
    │제어 루프│
    └─────────┘
```

---

## 📝 결론

전반적으로 **모듈화가 잘 되어 있고 구조가 명확**합니다. 하지만 몇 가지 **심각한 연동성 이슈**가 있어 즉시 수정이 필요합니다:

1. **이중 제어 문제**: `fire_module.py`와 `main.py`가 동시에 LED/부저를 제어하여 충돌 가능
2. **cleanup 함수 누락**: 여러 모듈에 cleanup 함수가 없어 리소스 해제 문제 가능
3. **스레드 안전성**: 전역 변수 접근 시 Lock 부재

이러한 이슈들을 수정하면 시스템의 안정성과 예측 가능성이 크게 향상될 것입니다.

