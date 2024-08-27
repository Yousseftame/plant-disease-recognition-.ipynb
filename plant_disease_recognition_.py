# -*- coding: utf-8 -*-
"""plant disease recognition .ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1blGOwviRXafMGBSw4w0oRfoDC7PU7ivK

![pawel-czerwinski-lWBZ01XRRoI-unsplash.jpg](attachment:pawel-czerwinski-lWBZ01XRRoI-unsplash.jpg)

#  introduction to the  Plant Disease Recognition Dataset
This dataset contains three labels: **Healthy**, **Early blight**, **Late blight** referring to plant conditions.
There is a total of 2252 images divided into train, test, and validation sets.

# Early Blight
Early blight are plant diseases caused by pathogenic fungi of the order Pucciniales (previously known as Uredinales). An estimated 168 rust genera and approximately 7,000 species, more than half of which belong to the genus Puccinia, are currently accepted.[1] Rust fungi are highly specialized plant pathogens with several unique features. Taken as a group, rust fungi are diverse and affect many kinds of plants. However, each species has a very narrow range of hosts and cannot be transmitted to non-host plants. In addition, most rust fungi cannot be grown easily in pure culture. A single species of rust fungi may be able to infect two different plant hosts in different stages of its life cycle, and may produce up to five morphologically and cytologically distinct spore-producing structures viz., spermogonia, aecia, uredinia, telia, and basidia in successive stages of reproduction.[2] Each spore type is very host specific, and can typically infect only one kind of plant. Rust fungi are obligate plant pathogens that only infect living plants. Infections begin when a spore lands on the plant surface, germinates, and invades its host. Infection is limited to plant parts such as leaves, petioles, tender shoots, stem, fruits, etc. Plants with severe rust infection may appear stunted, chlorotic (yellowed), or may display signs of infection such as rust fruiting bodies. Rust fungi grow intracellularly, and make spore-producing fruiting bodies within or, more often, on the surfaces of affected plant parts. Some rust species form perennial systemic infections that may cause plant deformities such as growth retardation, witch's broom, stem canker, galls, or hypertrophy of affected plant parts. Rusts get their name because they are most commonly observed as deposits of powdery rust-coloured or brown spores on plant surfaces. The Roman agricultural festival Robigalia (April 25) has ancient origins in combating wheat rust.

![early.PNG](attachment:early.PNG)

# Late Blight
Late blight mildew is a fungal disease that affects a wide range of plants. Powdery mildew diseases are caused by many different species of fungi in the order Erysiphales. Powdery mildew is one of the easier plant diseases to identify, as its symptoms are quite distinctive. Infected plants display white powdery spots on the leaves and stems. The lower leaves are the most affected, but the mildew can appear on any above-ground part of the plant. As the disease progresses, the spots get larger and denser as large numbers of asexual spores are formed, and the mildew may spread up and down the length of the plant. Powdery mildew grows well in environments with high humidity and moderate temperatures. Greenhouses provide an ideal moist, temperate environment for the spread of the disease. This causes harm to agricultural and horticultural practices where powdery mildew may thrive in a greenhouse setting. In an agricultural or horticultural setting, the pathogen can be controlled using chemical methods, bio organic methods, and genetic resistance. It is important to be aware of powdery mildew and its management as the resulting disease can significantly reduce important crop yields.

![late.PNG](attachment:late.PNG)

# Import requirements ( dependency)
"""

import tensorflow as tf
from tensorflow.keras import models,layers
import matplotlib.pyplot as plt

IMAGE_SIZE = 256
BATCH_SIZE = 32
CHANNELS = 3
EPOCHES = 10

dataset = tf.keras.preprocessing.image_dataset_from_directory(
    "PlantVillage",
    shuffle=True,                                    # to make images random
    image_size= (IMAGE_SIZE,IMAGE_SIZE),
    batch_size= BATCH_SIZE

)

class_names = dataset.class_names
class_names

len(dataset)                                        # 2152 / 32

for image_batch , label_batch in dataset.take(1): # It will retrieve only the N number of Batches  directly.
    print(image_batch[0].numpy())                  # matrix of every image in batch   (0,255)
    print(image_batch.shape)                       # shape of batch
    print(label_batch.numpy())                     # label for every batch

"""# data visualization"""

plt.figure(figsize=(15,15))
for image_batch , label_batch in dataset.take(1):
    for i in range(12):
        ax = plt.subplot(3,4,i+1)
        plt.imshow(image_batch[i].numpy().astype("uint8"))
        plt.title(class_names[label_batch[i]])
        plt.axis("off")

"""# Split Data collection
training ==> 80%
test     ==> 10%
validation =>10%

"""

def get_dataset_spliting(ds):
    '''A function to split a data set into 3 parts'''
    train_size = 0.8
    len(ds)*train_size
    train_ds = ds.take(54)                   # arr[:54]
    len(train_ds)

    test_ds =dataset.skip(54)                   # arr[54:]
    len(test_ds)


    val_size = 0.1
    len(ds)*val_size
    val_ds =test_ds.take(6)
    len(val_ds)

    test_ds = test_ds.skip(6)
    len(test_ds)

    return train_ds , val_ds , test_ds

train_ds , val_ds , test_ds = get_dataset_spliting(dataset)

len(train_ds),len(val_ds),len(test_ds)

"""# Optimize Dataset For Fast Training Perfromance"""

''' leting tensorflow determine how many batces to load while GPU is training to improve performance'''

train_ds =train_ds.cache().shuffle(1000).prefetch(buffer_size=tf.data.AUTOTUNE)

val_ds =val_ds.cache().shuffle(1000).prefetch(buffer_size=tf.data.AUTOTUNE)

test_ds =test_ds.cache().shuffle(1000).prefetch(buffer_size=tf.data.AUTOTUNE)

"""# Pre-processing dataset"""

resize_and_rescale = tf.keras.Sequential([
    layers.experimental.preprocessing.Resizing(IMAGE_SIZE,IMAGE_SIZE), # to resize any image not 255 into 255
    layers.experimental.preprocessing.Rescaling(1.0/255) #To rescale an input in the [0, 255] To make it Rgb
])

"""# Data Augmentation"""

data_augmentation = tf.keras.Sequential([
    layers.experimental.preprocessing.RandomFlip("horizontal_and_vertical"), # API
    layers.experimental.preprocessing.RandomRotation(0.2)                    # API
])

"""#  Build our Convolutional Neural Network

"""

input_shape= (BATCH_SIZE,IMAGE_SIZE,IMAGE_SIZE,CHANNELS)
n_classes = 3

model = models.Sequential([
    resize_and_rescale,
    data_augmentation,
    layers.Conv2D(32,(3,3),activation='relu',input_shape=input_shape),        # Convolution layer 1
    layers.MaxPooling2D((2,2)),               # Convolution layer 2
    layers.Conv2D(64,(3,3),activation='relu',input_shape=input_shape),
    layers.MaxPooling2D((2,2)),              # # Convolution layer 3
    layers.Conv2D(64,(3,3),activation='relu',input_shape=input_shape),
    layers.MaxPooling2D((2,2)),              # Convolution layer 4
    layers.Conv2D(64,(3,3),activation='relu',input_shape=input_shape),
    layers.MaxPooling2D((2,2)),              # Convolution layer 5
    layers.Conv2D(64,(3,3),activation='relu',input_shape=input_shape),
    layers.MaxPooling2D((2,2)),              # Convolution layer 6
    layers.Conv2D(64,(3,3),activation='relu',input_shape=input_shape),
    layers.MaxPooling2D((2,2)),
    layers.Flatten(),                        #  Flatten Layers
    layers.Dense(64 , activation='relu'),      # Dense activation layer
    layers.Dense(n_classes ,activation ='softmax' ), # last layer will have 3 neurous


])

model.build(input_shape=input_shape) #API model

model.summary()

"""# Define Optimizer"""

model.compile(
    optimizer ='adam',
    loss = tf.keras.losses.SparseCategoricalCrossentropy(from_logits=False),
    metrics =['accuracy']


)

history = model.fit(
    train_ds,
    epochs=EPOCHES,
    batch_size=BATCH_SIZE,
    verbose=1,
    validation_data=val_ds



)

scores = model.evaluate(test_ds)

scores

history.history.keys()

history.history['accuracy']

acc = history.history['accuracy']
val_acc = history.history['val_accuracy']

loss = history.history['loss']
val_loss = history.history['val_loss']

# show accuracy graph
plt.figure(figsize=(8,8))
plt.subplot(1,2,1)
plt.plot(range(EPOCHES),acc,label='Training Accuracy')
plt.plot(range(EPOCHES),val_acc,label='Validation Accuracy')
plt.legend(loc='lower right')
plt.title('Training and Validation accuracy')

# show loss graph
plt.subplot(1,2,2)
plt.plot(range(EPOCHES),loss,label='Training loss')
plt.plot(range(EPOCHES),val_loss,label='Validation loss')
plt.legend(loc='upper right')
plt.title('Training and Validation loss')

"""# Make a Prediction"""

import numpy as np


for image_batch, label_batch in test_ds.take(1):
    first_image = image_batch[0].numpy().astype('uint8')
    first_label = label_batch[0].numpy()

    print("First image to predict")
    plt.imshow(first_image)
    print("Actual label :",class_names[first_label])

    batch_prediction =model.predict(image_batch)
    #print ("predicted label : ",(batch_prediction[0]))
    #print(np.argmax(batch_prediction[0]))
    print ("predicted label : ",class_names[np.argmax(batch_prediction[0])])





    plt.axis('off')

model_version=1
model.save(f"../models/{model_version}")
