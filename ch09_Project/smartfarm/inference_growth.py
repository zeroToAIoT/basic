# file: inference_growth.py
# 라즈베리파이에서 plant_growth.tflite 모델을 이용한 식물 성장 단계 추론

from PIL import Image
import numpy as np
import tflite_runtime.interpreter as tflite
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
from config import MODEL_PATH, GROWTH_LABELS   # config.py에서 경로와 라벨 불러오기

# 인터프리터와 입출력 정보는 lazy-loading 방식으로 초기화
interpreter = None
input_details = None
output_details = None
IMG_HEIGHT, IMG_WIDTH = None, None


def load_model():
    """모델을 최초 1회만 로드"""
    global interpreter, input_details, output_details, IMG_HEIGHT, IMG_WIDTH
    if interpreter is None:
        interpreter = tflite.Interpreter(model_path=MODEL_PATH)
        interpreter.allocate_tensors()
        input_details = interpreter.get_input_details()
        output_details = interpreter.get_output_details()
        input_shape = input_details[0]['shape']
        IMG_HEIGHT, IMG_WIDTH = input_shape[1], input_shape[2]


def analyze_growth_stage(image_path):
    try:
        # 모델 로드 (최초 1회만 실행)
        load_model()

        # 이미지 열기 및 리사이즈
        image = Image.open(image_path).convert("RGB")
        image = image.resize((IMG_WIDTH, IMG_HEIGHT))

        # NumPy 배열 변환 및 MobileNetV2 전처리 적용
        image = np.array(image, dtype=np.float32)
        image = preprocess_input(image)

        # 배치 차원 추가
        image = np.expand_dims(image, axis=0)

        # 모델 입력 설정
        interpreter.set_tensor(input_details[0]['index'], image)

        # 추론 실행
        interpreter.invoke()

        # 결과 가져오기
        output_data = interpreter.get_tensor(output_details[0]['index'])

        # 가장 높은 확률의 클래스 선택
        growth_level = int(np.argmax(output_data)) + 1
        confidence = float(np.max(output_data))

        label = GROWTH_LABELS.get(growth_level, "Unknown Stage")

        print(f"Predicted Growth Stage: {growth_level} - {label} (confidence: {confidence:.2f})")
        return growth_level, confidence