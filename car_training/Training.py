print('Setting UP')
import matplotlib.pyplot as plt
import os
import random
import cv2
import numpy as np
from tensorflow import keras

IMG_SIZE1 = 200
IMG_SIZE2 = 60
EPOCHS = 5
LOSS_THRESHOLD = 0.34

TRAIN_DIR = 'C:/Users/Admin/PycharmProjects/car_training/DataCollected'
OWN_IMAGE_PATH = 'C:/Users'

train_img_count = 0
train_images = []
CATEGORIES = ["Left", "Right", "Forward"]


class myCallback(keras.callbacks.Callback):
    def on_epoch_end(self, epoch, logs={}):
        if logs.get('val_loss') < LOSS_THRESHOLD:
            print("\nReached %2.2f%% accuracy, so stopping training!!" % (LOSS_THRESHOLD * 100))
            self.model.stop_training = True


print("Processing Images...")
for categories in CATEGORIES:
    train_img_path = os.path.join(TRAIN_DIR, categories)
    print(train_img_path)
    class_num = CATEGORIES.index(categories)
    for img in os.listdir(train_img_path):
        train_img_count += 1
        try:
            train_img_array = cv2.imread(os.path.join(train_img_path, img), cv2.IMREAD_GRAYSCALE)
            new_test_array = cv2.resize(train_img_array, (IMG_SIZE1, IMG_SIZE2))
        except:
            pass
        train_images.append([new_test_array, class_num])
print(f"{train_img_count} Train Images")

random.shuffle(train_images)

X = []
y = []

for features, labels in train_images:
    X.append(features)
    y.append(labels)

X = np.array(X).reshape(-1, IMG_SIZE1, IMG_SIZE2, 1)

y = np.array(y)

X = X / 255.0

print(X)

callbacks = myCallback()

print("Training...")
model = keras.Sequential([

    keras.layers.Conv2D(24, (3, 3), activation="relu"),
    keras.layers.MaxPooling2D(2, 2),

    keras.layers.Conv2D(30, (3, 3), activation="relu"),

    keras.layers.Conv2D(32, (3, 3), activation="relu"),
    keras.layers.Dropout(0.6),

    keras.layers.Flatten(),
    keras.layers.Dense(28, activation="relu"),

    keras.layers.Dense(16, activation="relu"),

    keras.layers.Dense(12, activation="relu"),

    keras.layers.Dense(8, activation="relu"),
    keras.layers.Dropout(0.4),

    keras.layers.Dense(3, activation="softmax")  # normal softmax
])

model.compile(optimizer='adam', loss=keras.losses.sparse_categorical_crossentropy, metrics=['accuracy'])

history = model.fit(X, y, batch_size=150, epochs=EPOCHS, callbacks=[callbacks], validation_split=0.25)

print(history.history.keys())
print(history.history)
# summarize history for accuracy
plt.plot(history.history['accuracy'])
plt.plot(history.history['val_accuracy'])
plt.title('model accuracy')
plt.ylabel('accuracy')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper left')
plt.show()
# summarize history for loss
plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.title('model loss')
plt.ylabel('loss')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper left')
plt.show()

save_string = input("Save: Y or N")
if save_string == "y":
    model.save('modelv3.h5')
else:
    pass
