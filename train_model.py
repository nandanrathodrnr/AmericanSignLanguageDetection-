import numpy as np
import os
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense

DATA_DIR = "data"
labels = os.listdir(DATA_DIR)
label_map = {label: i for i, label in enumerate(labels)}

X, y = [], []

for label in labels:
    for file in os.listdir(os.path.join(DATA_DIR, label)):
        data = np.load(os.path.join(DATA_DIR, label, file))
        X.append(data)
        y.append(label_map[label])

X = np.array(X)
y = np.array(y)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

model = Sequential([
    Dense(128, activation='relu', input_shape=(63,)),
    Dense(64, activation='relu'),
    Dense(len(labels), activation='softmax')
])

model.compile(
    optimizer='adam',
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy']
)

model.fit(X_train, y_train, epochs=20, validation_data=(X_test, y_test))
model.save("asl_model.h5")

print("Model trained and saved!")
