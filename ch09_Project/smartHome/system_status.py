# file: system_status.py
# Shared system status module for inter-module communication

# 시스템 활성 상태를 공유하기 위한 모듈
# 다른 모듈에서 import하여 시스템 상태를 확인할 수 있음

_system_active = False

def set_system_active(status: bool):
    """시스템 활성 상태를 설정"""
    global _system_active
    _system_active = status

def is_system_active() -> bool:
    """시스템이 활성화되어 있는지 확인"""
    return _system_active

