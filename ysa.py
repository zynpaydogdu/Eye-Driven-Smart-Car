import os
import cv2
import numpy as np
import tensorflow as tf
import socket
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import time

img_size = 100
batch_size = 32
epochs = 20

data_path = 'C:/Users/aysez/Desktop/Eye-Driven-Smart-Car/Data'

datagen = ImageDataGenerator(rescale=1./255)
train_data = datagen.flow_from_directory(
    data_path,
    target_size=(img_size, img_size),
    batch_size=batch_size,
    class_mode='categorical'
)

model = Sequential([
    Conv2D(32, (3,3), activation='relu', input_shape=(img_size, img_size, 3)),
    MaxPooling2D(),
    Conv2D(64, (3,3), activation='relu'),
    MaxPooling2D(),
    Flatten(),
    Dense(128, activation='relu'),
    Dropout(0.3),
    Dense(4, activation='softmax')  
])

model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])


print("📈 Model eğitiliyor...")
model.fit(train_data, epochs=epochs)
model.save("eye_direction_model.h5")
print("✅ Model kaydedildi.")

def send_command(command):
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(("raspberrypi.local", 5000))  
        client.sendall(command.encode())
        client.close()
        print(f"📤 Komut gönderildi: {command}")
    except Exception as e:
        print(f"❌ Komut gönderilemedi: {e}")

classes = ['sag', 'sol', 'duz', 'dur']

model = load_model("eye_direction_model.h5")

cap = cv2.VideoCapture(0)

print("🎥 Kamera açıldı, gerçek zamanlı göz takibi başlıyor...")

last_prediction = None
last_time = time.time()

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    roi = frame[100:300, 200:400]
    roi_resized = cv2.resize(roi, (img_size, img_size))
    roi_normalized = roi_resized / 255.0
    roi_input = np.expand_dims(roi_normalized, axis=0)

    prediction = model.predict(roi_input, verbose=0)
    class_index = np.argmax(prediction)
    predicted_label = classes[class_index]

    if predicted_label != last_prediction or time.time() - last_time > 2:
        send_command(predicted_label)
        last_prediction = predicted_label
        last_time = time.time()

    cv2.rectangle(frame, (200, 100), (400, 300), (0, 255, 0), 2)
    cv2.putText(frame, f"Direction: {predicted_label}", (30, 50),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)

    cv2.imshow("Eye Direction Estimation", frame)

    if cv2.waitKey(5) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()