import tensorflow
from tensorflow import keras
import numpy as np
import random
from time import time
import os
from sklearn.model_selection import train_test_split
import cv2
import glob
import sys
import matplotlib.pyplot as plt

EPOCHS = 100
data_path = "training_data/*.npz"


def load_data(input_size, path):
    print("Loading training data...")

    # load training data
    X = np.empty((0, 38400))
    y = np.empty((0, 4))
    training_data = glob.glob(path)

    # if no data, exit
    if not training_data:
        print("Data not found, exit")
        sys.exit()

    for single_npz in training_data:
        with np.load(single_npz) as data:
            train = data['train']
            train_labels = data['train_labels']
        X = np.vstack((X, train))
        y = np.vstack((y, train_labels))

    print("Image array shape: ", X.shape)
    print("Label array shape: ", y.shape)


    # normalize data
    X = X / 255

    # train validation split, 7:3
    return X, y


X_train, y_train = load_data(120 * 320, data_path)

model = keras.Sequential([

    keras.layers.Conv2D(64, (3, 3), activation="relu", input_shape=(1, 497, 2, 64)),
    keras.layers.MaxPooling2D(2, 2),

    keras.layers.Conv2D(128, (3, 3), activation="relu"),
    keras.layers.MaxPooling2D(2, 2),

    keras.layers.Conv2D(256, (3, 3), activation="relu"),
    keras.layers.MaxPooling2D(2, 2),

    keras.layers.Flatten(),
    keras.layers.Dense(256, activation="relu"),
    keras.layers.Dropout(0.8),

    keras.layers.Dense(128, activation="relu"),

    keras.layers.Flatten(),
    keras.layers.Dense(128, activation="relu"),
    keras.layers.Dropout(0.8),

    keras.layers.Dense(4, activation="softmax")
])

model.compile(optimizer='adam', loss=keras.losses.sparse_categorical_crossentropy, metrics=['accuracy'])

model.fit(X_train, y_train, batch_size=120, epochs=EPOCHS, validation_split=0.2)

model.save('training/')
