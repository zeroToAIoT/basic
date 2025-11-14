# SmartHome 프로젝트 연동성 검토 보고서

## 📋 검토 개요
- **검토 일자**: 2024
- **검토 범위**: smartHome 프로젝트 전체 모듈 간 연동성
- **검토 목적**: 모듈 간 통신, 상태 공유, 의존성 관리, 스레드 안전성 확인

---

## 🔴 심각한 연동성 이슈

### 1. **datetime import 위치 오류** (main.py)
**위치**: `main.py` 135번째 줄  
**문제**: 
- `datetime`이 187번째 줄의 `if __name__ == '__main__'` 블록 안에서만 import됨
- 하지만 `_monitor_and_control_loop()` 함수(135번째 줄)에서 `datetime.now()` 사용
- 시스템 활성화 시 `NameError: name 'datetime' is not defined` 발생

**영향도**: 🔴 **매우 높음** - 시스템이 시작되지 않음

**수정 필요**:
```python
# main.py 상단에 추가
from datetime import datetime
```

---

### 2. **모니터링 루프가 시스템 상태를 확인하지 않음**
**위치**: 모든 모니터링 모듈  
**문제**:
- `monitor_pir_sensors()`, `monitor_fire_sensor()`, `monitor_light_sensor()`, `monitor_temp_hum_sensor()`, `morningCall_play()`, `multiFnd_display_time()` 모두 `while True` 루프 사용
- `smartHome_active` 상태를 확인하지 않아 시스템 비활성화 후에도 계속 실행됨
- 스레드가 정상적으로 종료되지 않음

**영향도**: 🔴 **높음** - 리소스 누수, 정상 종료 불가

**수정 필요**: 각 모니터링 함수에 `smartHome_active` 체크 추가

---

### 3. **fire_module.py의 직접 제어로 인한 이중 제어 문제**
**위치**: `fire_module.py` 33-34, 40-41번째 줄  
**문제**:
- `fire_module.py`가 `led_module`과 `buzzer_module`을 직접 import하여 제어
- 동시에 `main.py`의 `_monitor_and_control_loop()`에서도 같은 모듈 제어
- 두 곳에서 동시에 제어하여 충돌 가능성

**영향도**: 🟡 **중간** - LED/부저 제어가 예상과 다르게 동작할 수 있음

**권장 수정**: 
- `fire_module.py`는 상태만 감지하고, 제어는 `main.py`에서만 수행
- 또는 명확한 우선순위 규칙 설정

---

### 4. **스레드 안전성 문제 - 전역 변수 접근**
**위치**: 모든 센서 모듈  
**문제**:
- `_motion_detected_at`, `_fire_alert_active`, `_current_light_value`, `_current_temperature`, `_current_humidity` 등이 전역 변수로 관리됨
- 여러 스레드에서 동시에 읽기/쓰기 가능하지만 Lock 없음
- `main.py`의 `_system_status`만 Lock이 있음

**영향도**: 🟡 **중간** - 데이터 일관성 문제 가능성

**권장 수정**: 각 모듈의 전역 변수 접근에 Lock 추가 또는 `main.py`의 `_system_status`로 통합

---

### 5. **bluedot_module.py에서 존재하지 않는 함수 import**
**위치**: `main.py` 26번째 줄  
**문제**:
```python
from bluedot_module import bd, activate_system, deactivate_system, ...
```
- `activate_system`, `deactivate_system` 함수가 `bluedot_module.py`에 정의되어 있지 않음
- 실제로는 `set_control_functions`만 사용됨

**영향도**: 🟠 **낮음** - ImportError 발생 (현재는 사용하지 않아 문제 없을 수 있음)

**수정 필요**: 사용하지 않는 import 제거

---

## 🟡 개선 권장 사항

### 6. **모듈 간 의존성 관리**
**현재 구조**:
- `fire_module.py` → `led_module.py`, `buzzer_module.py` 직접 import
- `pir_module.py` → `camera_module.py` 직접 import
- `main.py` → 모든 모듈 import

**권장 사항**: 
- 모듈 간 직접 제어보다는 이벤트/콜백 패턴 또는 메시지 큐 사용
- 또는 명확한 계층 구조 정의 (센서 → 제어 → 액추에이터)

---

### 7. **에러 처리 및 복구 메커니즘**
**문제**:
- 모니터링 루프에서 예외 발생 시 `sleep(5)` 후 재시도하지만, 시스템 상태 확인 없이 무한 재시도
- 특정 센서 오류가 전체 시스템에 영향

**권장 사항**: 
- 센서별 독립적인 에러 카운터 및 복구 로직
- 심각한 오류 시 해당 모듈만 비활성화

---

### 8. **cleanup 함수 일관성**
**현재 상태**:
- 대부분의 모듈에 `cleanup()` 함수가 있음
- 하지만 모니터링 루프 내부 리소스 정리가 불완전할 수 있음

**권장 사항**: 
- 각 모듈의 cleanup이 모든 리소스를 확실히 해제하는지 확인
- 특히 무한 루프를 가진 모듈의 정상 종료 보장

---

### 9. **config.py 경로 하드코딩**
**위치**: `config.py` 39번째 줄  
**문제**:
```python
BASE_DIR = '/home/pi/smartHome'
```
- 절대 경로 하드코딩으로 다른 환경에서 실행 어려움

**권장 사항**: 
- 상대 경로 또는 환경 변수 사용
- `os.path.dirname(__file__)` 사용

---

### 10. **button_module_advanced.py의 순환 import 위험**
**위치**: `button_module_advanced.py`  
**문제**:
```python
from main import activate, deactivate
```
- `main.py`가 `button_module.py`를 import하는데, `button_module_advanced.py`가 `main.py`를 import하면 순환 import 가능성

**영향도**: 🟠 **낮음** - 현재는 사용되지 않는 것으로 보임

---

## ✅ 잘 구현된 부분

1. **모듈화 구조**: 각 기능이 명확히 분리되어 있음
2. **config.py 중앙 관리**: GPIO 핀, 임계값 등이 한 곳에서 관리됨
3. **함수 기반 인터페이스**: 모듈 간 통신이 함수 호출로 명확함
4. **cleanup 패턴**: 대부분의 모듈에 리소스 정리 함수가 있음
5. **스레드 기반 아키텍처**: 동시성 처리를 위한 구조가 있음

---

## 🔧 우선순위별 수정 권장사항

### 즉시 수정 필요 (P0) - ✅ **수정 완료**
1. ✅ `main.py`에 `from datetime import datetime` 추가 - **완료**
2. ✅ 모든 모니터링 루프에 `smartHome_active` 체크 추가 - **완료**
   - `system_status.py` 모듈 생성하여 시스템 상태 공유
   - 모든 모니터링 함수에 `is_system_active()` 체크 추가
3. ✅ `main.py`에서 사용하지 않는 import 제거 - **완료**

### 단기 개선 (P1)
4. ✅ `fire_module.py`의 직접 제어 로직 재검토
5. ✅ 전역 변수 접근에 Lock 추가
6. ✅ `config.py` 경로를 상대 경로로 변경

### 중기 개선 (P2)
7. ✅ 모듈 간 의존성 구조 개선
8. ✅ 에러 처리 및 복구 메커니즘 강화
9. ✅ 테스트 코드 추가

---

## 📝 결론

전반적으로 **모듈화가 잘 되어 있고 구조가 명확**합니다. 하지만 몇 가지 **심각한 연동성 이슈**가 있어 즉시 수정이 필요합니다:

1. **datetime import 오류**로 인해 시스템이 시작되지 않을 수 있음
2. **모니터링 루프가 시스템 상태를 무시**하여 정상 종료가 어려움
3. **이중 제어 문제**로 인한 예측 불가능한 동작 가능성

이러한 이슈들을 수정하면 시스템의 안정성과 예측 가능성이 크게 향상될 것입니다.

