# file: train_finetuning_1.py
import tensorflow as tf
from tensorflow.keras.applications import MobileNetV2, preprocess_input
from tensorflow.keras import layers, models
from tensorflow.keras.preprocessing import image_dataset_from_directory

# 1. 데이터셋 불러오기
train_ds = image_dataset_from_directory(
    "dataset/train",
    image_size=(224, 224),
    batch_size=32
)
val_ds = image_dataset_from_directory(
    "dataset/val",
    image_size=(224, 224),
    batch_size=32
)

# 2. 전처리 (MobileNetV2 권장 입력 범위: [-1, 1])
train_ds = train_ds.map(lambda x, y: (preprocess_input(x), y))
val_ds = val_ds.map(lambda x, y: (preprocess_input(x), y))

# 3. 사전 학습된 모델 불러오기
base_model = MobileNetV2(weights='imagenet', include_top=False, input_shape=(224,224,3))
base_model.trainable = False   # 일부 레이어 고정

# 4. 파인튜닝 모델 구성
num_classes = 4  # 성장 단계 클래스 수
model = models.Sequential([
    base_model,
    layers.GlobalAveragePooling2D(),
    layers.Dense(num_classes, activation='softmax')
])

# 5. 컴파일 & 학습
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
history = model.fit(train_ds, validation_data=val_ds, epochs=10)

# 6. TFLite 변환
converter = tf.lite.TFLiteConverter.from_keras_model(model)
tflite_model = converter.convert()
with open("plant_growth.tflite", "wb") as f:
    f.write(tflite_model)

print("✅ TFLite 모델 저장 완료: plant_growth.tflite")