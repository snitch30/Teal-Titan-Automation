 #!/usr/bin/env python3 # -*- coding: utf-8 -*-
"""
Code for CNN Training
@author: stejasmunees
"""
#Building the CNN
from keras.models import Sequential
from keras.layers import Convolution2D
from keras.layers import MaxPooling2D
from keras.layers import Flatten
from keras.layers import Dense
from keras.layers import LeakyReLU
from keras.layers import Dropout
from keras.layers import BatchNormalization
from keras.optimizers import Nadam

#Initialising the CNN
classifier = Sequential()
#Step 1 - Convolution
classifier.add(Convolution2D(filters=32,kernel_size=[3,3],input_shape=(64,64,3),activation='relu'))
classifier.add(BatchNormalization())
#Step 2 - Pooling
classifier.add(MaxPooling2D(pool_size=(2,2),strides=2))
#Adding another Convolutional Layer for better accuracy
classifier.add(Convolution2D(filters=64,kernel_size=[3,3],activation='relu'))
classifier.add(BatchNormalization())
classifier.add(MaxPooling2D(pool_size=(2,2),strides=2))
#Adding another Convolutional Layer for better accuracy
classifier.add(Convolution2D(filters=32,kernel_size=[3,3],activation='relu'))
classifier.add(BatchNormalization())
classifier.add(MaxPooling2D(pool_size=(2,2),strides=2))
#Step 3 - Flattening
classifier.add(Flatten())
#Step 4 - Fully Connected Layers
classifier.add(Dense(units= 32))
#classifier.add(Dropout(rate=0.4))
classifier.add(Dense(units= 16)) #, activation='relu'
classifier.add(LeakyReLU(alpha=0.005))
#classifier.add(Dropout(rate=0.2))
classifier.add(Dense(units= 2, activation='softmax'))
#Optimizer
optimizer = Nadam(lr=0.0001, beta_1=0.9, beta_2=0.999, epsilon=None, schedule_decay=0.004)
#Compiling the CNN
classifier.compile(optimizer=optimizer,loss = 'categorical_crossentropy', metrics=['accuracy'])

#Part 2 - Fitting the CNN to the images
from keras.preprocessing.image import ImageDataGenerator
train_datagen=ImageDataGenerator(rescale=1./255, shear_range=0.2, zoom_range=0.2, horizontal_flip=True)
test_datagen=ImageDataGenerator(rescale=1./255)
training_set = train_datagen.flow_from_directory('/floyd/input/dat2/training_set', target_size=(64,64), batch_size=32,class_mode='categorical')
test_set = test_datagen.flow_from_directory('/floyd/input/dat2/test_set', target_size=(64,64), batch_size=32,class_mode='categorical')
# Fitting the compiled model
classifier.fit_generator(training_set, steps_per_epoch=195, epochs=30, validation_data=test_set, validation_steps=25)

#Saving the model
import h5py
# serialize model to JSON
model_json = classifier.to_json()
with open("teal_07.json", "w") as json_file:
   json_file.write(model_json)
# serialize weights to HDF5
classifier.save_weights("teal_07.h5")
print("Saved model to disk")
