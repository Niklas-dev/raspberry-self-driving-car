from tensorflow import keras

# Epochs / Accuracy / Val_Accuracy
# 100 / 0.9641 / 0.9123
model = keras.Sequential([
    keras.layers.Conv2D(24, (3, 3), activation="relu"),
    keras.layers.MaxPooling2D(3, 3),

    keras.layers.Conv2D(36, (3, 3), activation="relu"),
    keras.layers.Conv2D(48, (3, 3), activation="relu"),
    keras.layers.Conv2D(48, (3, 3), activation="relu"),
    keras.layers.Conv2D(64, (3, 3), activation="relu"),
    keras.layers.Conv2D(64, (3, 3), activation="relu"),

    keras.layers.Flatten(),
    keras.layers.Dense(128, activation="relu"),
    keras.layers.Dropout(0.3),
    keras.layers.Dense(128, activation="relu"),
    keras.layers.Dense(128, activation="relu"),

    keras.layers.Dense(64, activation="relu"),

    keras.layers.Dense(32, activation="relu"),
    keras.layers.Dropout(0.3),

    keras.layers.Flatten(),
    keras.layers.Dense(32, activation="relu"),
    keras.layers.Dense(32, activation="relu"),
    keras.layers.Dense(16, activation="relu"),
    keras.layers.Dense(16, activation="relu"),

    keras.layers.Dense(3, activation="softmax")
])

# 100 / 0.9694 / 0.9042
model = keras.Sequential([

    keras.layers.Conv2D(24, (3, 3), activation="relu"),
    keras.layers.MaxPooling2D(3, 3),

    keras.layers.Conv2D(36, (3, 3), activation="relu"),
    keras.layers.Conv2D(48, (3, 3), activation="relu"),
    keras.layers.Conv2D(64, (3, 3), activation="relu"),
    keras.layers.Conv2D(64, (3, 3), activation="relu"),


    keras.layers.Flatten(),
    keras.layers.Dense(128, activation="relu"),
    keras.layers.Dropout(0.3),

    keras.layers.Dense(64, activation="relu"),

    keras.layers.Dense(32, activation="relu"),
    keras.layers.Dropout(0.3),

    keras.layers.Flatten(),
    keras.layers.Dense(32, activation="relu"),
    keras.layers.Dense(16, activation="relu"),

    keras.layers.Dense(3, activation="softmax")
])

# 100 / 0.9607 / 0.9117
model = keras.Sequential([

    keras.layers.Conv2D(24, (3, 3), activation="relu"),
    keras.layers.MaxPooling2D(3, 3),

    keras.layers.Conv2D(36, (3, 3), activation="relu"),
    keras.layers.Conv2D(48, (3, 3), activation="relu"),
    keras.layers.Conv2D(64, (3, 3), activation="relu"),
    keras.layers.Conv2D(64, (3, 3), activation="relu"),
    keras.layers.Conv2D(128, (3, 3), activation="relu"),
    keras.layers.Conv2D(128, (3, 3), activation="relu"),
    keras.layers.Dropout(0.2),

    keras.layers.Flatten(),
    keras.layers.Dense(128, activation="relu"),
    keras.layers.Dropout(0.3),

    keras.layers.Dense(64, activation="relu"),

    keras.layers.Dense(32, activation="relu"),
    keras.layers.Dropout(0.3),

    keras.layers.Flatten(),
    keras.layers.Dense(32, activation="relu"),
    keras.layers.Dense(16, activation="relu"),
    keras.layers.Dense(16, activation="relu"),
    keras.layers.Dense(8, activation="relu"),

    keras.layers.Dense(3, activation="softmax")
])


# 100 / 0.9698 / 0.9203
model = keras.Sequential([

    keras.layers.Conv2D(24, (3, 3), activation="relu"),
    keras.layers.MaxPooling2D(3, 3),

    keras.layers.Conv2D(36, (3, 3), activation="relu"),
    keras.layers.Conv2D(48, (3, 3), activation="relu"),
    keras.layers.Conv2D(64, (3, 3), activation="relu"),
    keras.layers.Conv2D(64, (3, 3), activation="relu"),

    keras.layers.Flatten(),
    keras.layers.Dense(64, activation="relu"),
    keras.layers.Dropout(0.3),
    keras.layers.Flatten(),
    keras.layers.Dense(64, activation="relu"),

    keras.layers.Dense(32, activation="relu"),
    keras.layers.Dropout(0.3),

    keras.layers.Flatten(),
    keras.layers.Dense(32, activation="relu"),
    keras.layers.Dense(16, activation="relu"),
    keras.layers.Dense(8, activation="relu"),

    keras.layers.Dense(3, activation="softmax")
])