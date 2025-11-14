# file: train_finetuning_1.py
# 스마트팜 식물 성장 단계 분류 모델 파인튜닝

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import os
import glob
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
import seaborn as sns

# GPU 메모리 설정 (노트북에서 GPU 사용 시)
physical_devices = tf.config.experimental.list_physical_devices('GPU')
if len(physical_devices) > 0:
    tf.config.experimental.set_memory_growth(physical_devices[0], True)
    print("GPU 사용 가능")
else:
    print("CPU 사용")

# =============================================================================
# 1. 데이터 준비 및 전처리
# =============================================================================

def load_and_preprocess_data(data_dir, img_size=(224, 224)):
    """
    식물 이미지 데이터를 로드하고 전처리하는 함수
    
    Args:
        data_dir: 이미지 데이터가 있는 디렉토리 경로
        img_size: 이미지 크기 (기본값: 224x224)
    
    Returns:
        images: 전처리된 이미지 배열
        labels: 라벨 배열
        class_names: 클래스 이름 리스트
    """
    
    # 클래스 폴더 구조 확인
    class_folders = sorted([f for f in os.listdir(data_dir) 
                           if os.path.isdir(os.path.join(data_dir, f))])
    
    print(f"발견된 클래스: {class_folders}")
    
    images = []
    labels = []
    
    for class_idx, class_name in enumerate(class_folders):
        class_path = os.path.join(data_dir, class_name)
        image_files = glob.glob(os.path.join(class_path, "*.jpg")) + \
                     glob.glob(os.path.join(class_path, "*.png")) + \
                     glob.glob(os.path.join(class_path, "*.jpeg"))
        
        print(f"{class_name}: {len(image_files)}개 이미지")
        
        for img_path in image_files:
            try:
                # 이미지 로드 및 전처리
                img = Image.open(img_path).convert('RGB')
                img = img.resize(img_size)
                img_array = np.array(img) / 255.0  # 정규화
                
                images.append(img_array)
                labels.append(class_idx)
                
            except Exception as e:
                print(f"이미지 로드 오류 {img_path}: {e}")
                continue
    
    return np.array(images), np.array(labels), class_folders

# =============================================================================
# 2. 모델 정의 (MobileNetV2 기반)
# =============================================================================

def create_finetuning_model(num_classes, img_size=(224, 224)):
    """
    MobileNetV2 기반 파인튜닝 모델 생성
    
    Args:
        num_classes: 분류할 클래스 수
        img_size: 입력 이미지 크기
    
    Returns:
        model: 컴파일된 모델
    """
    
    # MobileNetV2 베이스 모델 로드 (사전 훈련된 가중치 사용)
    base_model = keras.applications.MobileNetV2(
        input_shape=(*img_size, 3),
        include_top=False,
        weights='imagenet'
    )
    
    # 베이스 모델의 가중치를 고정 (처음에는)
    base_model.trainable = False
    
    # 모델 구성
    model = keras.Sequential([
        base_model,
        layers.GlobalAveragePooling2D(),
        layers.Dropout(0.2),
        layers.Dense(128, activation='relu'),
        layers.Dropout(0.2),
        layers.Dense(num_classes, activation='softmax')
    ])
    
    # 모델 컴파일
    model.compile(
        optimizer=keras.optimizers.Adam(learning_rate=0.001),
        loss='sparse_categorical_crossentropy',
        metrics=['accuracy']
    )
    
    return model

# =============================================================================
# 3. 데이터 증강 (Data Augmentation)
# =============================================================================

def create_data_augmentation():
    """데이터 증강 레이어 생성"""
    
    data_augmentation = keras.Sequential([
        layers.RandomFlip("horizontal"),
        layers.RandomRotation(0.1),
        layers.RandomZoom(0.1),
        layers.RandomContrast(0.1),
    ])
    
    return data_augmentation

# =============================================================================
# 4. 학습률 스케줄링
# =============================================================================

def create_lr_schedule():
    """학습률 스케줄링 함수"""
    
    def lr_schedule(epoch):
        if epoch < 10:
            return 0.001
        elif epoch < 20:
            return 0.0001
        else:
            return 0.00001
    
    return lr_schedule

# =============================================================================
# 5. 콜백 함수들
# =============================================================================

def create_callbacks():
    """학습 콜백 함수들 생성"""
    
    callbacks = [
        # 조기 종료
        keras.callbacks.EarlyStopping(
            monitor='val_accuracy',
            patience=10,
            restore_best_weights=True
        ),
        
        # 학습률 스케줄링
        keras.callbacks.LearningRateScheduler(create_lr_schedule()),
        
        # 모델 체크포인트
        keras.callbacks.ModelCheckpoint(
            'best_plant_growth_model.h5',
            monitor='val_accuracy',
            save_best_only=True,
            verbose=1
        ),
        
        # 학습률 감소
        keras.callbacks.ReduceLROnPlateau(
            monitor='val_loss',
            factor=0.5,
            patience=5,
            min_lr=1e-7
        )
    ]
    
    return callbacks

# =============================================================================
# 6. 시각화 함수들
# =============================================================================

def plot_training_history(history):
    """학습 히스토리 시각화"""
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))
    
    # 정확도 그래프
    ax1.plot(history.history['accuracy'], label='Training Accuracy')
    ax1.plot(history.history['val_accuracy'], label='Validation Accuracy')
    ax1.set_title('Model Accuracy')
    ax1.set_xlabel('Epoch')
    ax1.set_ylabel('Accuracy')
    ax1.legend()
    
    # 손실 그래프
    ax2.plot(history.history['loss'], label='Training Loss')
    ax2.plot(history.history['val_loss'], label='Validation Loss')
    ax2.set_title('Model Loss')
    ax2.set_xlabel('Epoch')
    ax2.set_ylabel('Loss')
    ax2.legend()
    
    plt.tight_layout()
    plt.show()

def plot_confusion_matrix(y_true, y_pred, class_names):
    """혼동 행렬 시각화"""
    
    cm = confusion_matrix(y_true, y_pred)
    
    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
                xticklabels=class_names, yticklabels=class_names)
    plt.title('Confusion Matrix')
    plt.xlabel('Predicted')
    plt.ylabel('Actual')
    plt.show()

# =============================================================================
# 7. 메인 실행 함수
# =============================================================================

def main():
    """메인 실행 함수"""
    
    print("=== 스마트팜 식물 성장 단계 분류 모델 파인튜닝 ===")
    
    # 데이터 경로 설정 (실제 데이터 경로로 수정 필요)
    data_dir = "plant_growth_data"  # 데이터가 있는 폴더 경로
    
    if not os.path.exists(data_dir):
        print(f"데이터 디렉토리가 존재하지 않습니다: {data_dir}")
        print("데이터 구조 예시:")
        print("plant_growth_data/")
        print("├── stage1_seedling/")
        print("├── stage2_growth/")
        print("├── stage3_flowering/")
        print("└── stage4_fruiting/")
        return
    
    # 1. 데이터 로드
    print("\n1. 데이터 로드 중...")
    images, labels, class_names = load_and_preprocess_data(data_dir)
    
    print(f"총 이미지 수: {len(images)}")
    print(f"이미지 크기: {images.shape}")
    print(f"클래스 수: {len(class_names)}")
    
    # 2. 데이터 분할
    print("\n2. 데이터 분할 중...")
    X_train, X_test, y_train, y_test = train_test_split(
        images, labels, test_size=0.2, random_state=42, stratify=labels
    )
    
    X_train, X_val, y_train, y_val = train_test_split(
        X_train, y_train, test_size=0.2, random_state=42, stratify=y_train
    )
    
    print(f"훈련 데이터: {X_train.shape[0]}개")
    print(f"검증 데이터: {X_val.shape[0]}개")
    print(f"테스트 데이터: {X_test.shape[0]}개")
    
    # 3. 모델 생성
    print("\n3. 모델 생성 중...")
    model = create_finetuning_model(len(class_names))
    model.summary()
    
    # 4. 데이터 증강
    data_augmentation = create_data_augmentation()
    
    # 5. 첫 번째 단계: 베이스 모델 고정하고 분류기만 훈련
    print("\n4. 첫 번째 단계 훈련 (베이스 모델 고정)...")
    
    history1 = model.fit(
        X_train, y_train,
        validation_data=(X_val, y_val),
        epochs=20,
        batch_size=32,
        callbacks=create_callbacks(),
        verbose=1
    )
    
    # 6. 두 번째 단계: 베이스 모델의 일부 레이어 해제하고 파인튜닝
    print("\n5. 두 번째 단계 훈련 (파인튜닝)...")
    
    # 베이스 모델의 상위 레이어들만 훈련 가능하게 설정
    base_model = model.layers[0]
    base_model.trainable = True
    
    # 상위 레이어들만 훈련 가능하게 설정
    fine_tune_at = 100
    for layer in base_model.layers[:fine_tune_at]:
        layer.trainable = False
    
    # 학습률을 낮춰서 재컴파일
    model.compile(
        optimizer=keras.optimizers.Adam(learning_rate=0.0001),
        loss='sparse_categorical_crossentropy',
        metrics=['accuracy']
    )
    
    history2 = model.fit(
        X_train, y_train,
        validation_data=(X_val, y_val),
        epochs=10,
        batch_size=32,
        callbacks=create_callbacks(),
        verbose=1
    )
    
    # 7. 모델 평가
    print("\n6. 모델 평가 중...")
    
    # 테스트 데이터로 평가
    test_loss, test_accuracy = model.evaluate(X_test, y_test, verbose=0)
    print(f"테스트 정확도: {test_accuracy:.4f}")
    
    # 예측
    y_pred = model.predict(X_test)
    y_pred_classes = np.argmax(y_pred, axis=1)
    
    # 분류 리포트
    print("\n분류 리포트:")
    print(classification_report(y_test, y_pred_classes, target_names=class_names))
    
    # 8. 시각화
    print("\n7. 결과 시각화...")
    
    # 학습 히스토리 시각화
    plot_training_history(history1)
    plot_training_history(history2)
    
    # 혼동 행렬 시각화
    plot_confusion_matrix(y_test, y_pred_classes, class_names)
    
    # 9. 모델 저장
    print("\n8. 모델 저장 중...")
    
    # TensorFlow Lite 모델로 변환 (라즈베리파이용)
    converter = tf.lite.TFLiteConverter.from_keras_model(model)
    converter.optimizations = [tf.lite.Optimize.DEFAULT]
    tflite_model = converter.convert()
    
    with open('mobilenetv2_growth.tflite', 'wb') as f:
        f.write(tflite_model)
    
    print("모델 저장 완료:")
    print("- best_plant_growth_model.h5 (Keras 모델)")
    print("- mobilenetv2_growth.tflite (TensorFlow Lite 모델)")
    
    print("\n=== 파인튜닝 완료 ===")

# =============================================================================
# 8. 실행 부분
# =============================================================================

if __name__ == '__main__':
    main()