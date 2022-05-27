import numpy as np
import os
import PIL
import PIL.Image
import tensorflow as tf
import pathlib

MODELS_DIR = "models/"
data_dir = pathlib.Path('/media/win/Users/user/Downloads/fyp/extracted_images')

batch_size = 32
img_height = 45
img_width = 45

train_ds = tf.keras.utils.image_dataset_from_directory(
  data_dir,
  validation_split=0.2,
  label_mode='categorical',
  subset="training",
  color_mode="grayscale",
  seed=123,
  image_size=(img_height, img_width),
  batch_size=batch_size)


val_ds = tf.keras.utils.image_dataset_from_directory(
  data_dir,
  validation_split=0.2,
  subset="validation",
  label_mode="categorical",
    color_mode="grayscale",
  seed=123,
  image_size=(img_height, img_width),
  batch_size=batch_size)

test_dataset = val_ds.take(50)
val_ds = val_ds.skip(50)

print('Batches for testing -->', test_dataset.cardinality())
print('Batches for validating -->', val_ds.cardinality())

#normalization_layer = tf.keras.layers.Rescaling(1./255)

AUTOTUNE = tf.data.AUTOTUNE

train_ds = train_ds.cache().prefetch(buffer_size=AUTOTUNE)
val_ds = val_ds.cache().prefetch(buffer_size=AUTOTUNE)

num_classes = 29

model = tf.keras.Sequential([
  tf.keras.layers.Rescaling(1./255),
  tf.keras.layers.Conv2D(32, 3, activation='relu'),
  tf.keras.layers.MaxPooling2D(),
  tf.keras.layers.Conv2D(32, 3, activation='relu'),
  tf.keras.layers.MaxPooling2D(),
  #tf.keras.layers.DropOut(),
  tf.keras.layers.Conv2D(32, 3, activation='relu'),
  tf.keras.layers.MaxPooling2D(),
  tf.keras.layers.Flatten(),
  tf.keras.layers.Dense(128, activation='relu'),
  tf.keras.layers.Dense(num_classes)
])

model.compile(
  optimizer='adam',
  loss=tf.losses.CategoricalCrossentropy(from_logits=True),
  metrics=['accuracy'])

# model.compile(
#   optimizer='adam',
#   loss=tf.losses.SparseCategoricalCrossentropy(from_logits=True),
#   metrics=['accuracy'])


model.fit(
  train_ds,
  validation_data=val_ds,
  epochs=3
)

model_file = open("models/model_v.txt","r")
current_model_v = model_file.read().split(";")
model_file.close()
# example version = 1.1.2
temp_versions = current_model_v.split(".")
if int(temp_versions[2])<9:
    temp_versions[2] = str(int(temp_versions[2]) + 1)
else:    
    temp_versions[2] = '0'
    if int(temp_versions[1])<9:
        temp_versions[1] = str(int(temp_versions[1]) + 1)
    else:
        temp_versions[1] = '0'
        temp_versions[0] = str(int(temp_versions[0]) + 1)

new_model_version = temp_versions[0] + "." + temp_versions[1] + "." + temp_versions[2]

model_file = open("models/model_v.txt","w")
model_file.write(new_model_version)
model_name = "model" + new_model_version +".tf"
model_path = "models/" + str(model_name)
model.save(model_path)