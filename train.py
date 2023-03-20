import numpy as np
import cv2
from tensorflow.keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten
from keras.layers import Conv2D
from keras.optimizers import Adam
from keras.layers import MaxPooling2D
from keras.preprocessing.image import ImageDataGenerator

train_dir = 'data/train'
val_dir = 'data/test'
train_datagen = ImageDataGenerator(rescale=1./255)
val_datagen = ImageDataGenerator(rescale=1./255)
train_generator = train_datagen.flow_from_directory(
    train_dir,
    target_size=(48, 48),
    batch_size=64,
    color_mode="grayscale",
    class_mode='categorical')
validation_generator = val_datagen.flow_from_directory(
    val_dir,
    target_size=(48, 48),
    batch_size=64,
    color_mode="grayscale",
    class_mode='categorical'
)

emotion_mode = Sequential()
emotion_mode.add(Conv2D(32, kernel_size=(3, 3), activation='relu', input_shape=(48, 48, 1)))
emotion_mode.add(Conv2D(64, kernel_size=(3, 3), activation='relu'))
emotion_mode.add(MaxPooling2D(pool_size=(2, 2)))
emotion_mode.add(Dropout(0.25))
emotion_mode.add(Conv2D(128, kernel_size=(3, 3), activation='relu'))
emotion_mode.add(MaxPooling2D(pool_size=(2, 2)))
emotion_mode.add(Conv2D(128, kernel_size=(3, 3), activation='relu'))
emotion_mode.add(MaxPooling2D(pool_size=(2, 2)))
emotion_mode.add(Dropout(0.25))
emotion_mode.add(Flatten())
emotion_mode.add(Dense(1024, activation='relu'))
emotion_mode.add(Dropout(0.5))
emotion_mode.add(Dense(7, activation='softmax'))


emotion_mode.compile(loss='caregorical_crossentropy', optimizer=Adam(lr=0.0001, decay=1e-6), metrics=['accuracy'])

emotion_mode_infor = emotion_mode.fit_generator(
    train_generator,
    steps_per_epoch=28709 // 64,
    epochs=50,
    validation_data=validation_generator,
    validation_steps=7178 // 64)

emotion_mode.save_weights('model.h5')
