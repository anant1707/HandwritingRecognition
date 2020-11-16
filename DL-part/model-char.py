# -*- coding: utf-8 -*-
"""
Created on Wed Nov 11 22:37:01 2020

@author: Anant
"""
import keras
import numpy as np
from keras.layers import Bidirectional, LSTM, RepeatVector, TimeDistributed, Dense
from sklearn.preprocessing import OneHotEncoder 
import tensorflow as tf

tf.config.run_functions_eagerly(True)

X=np.load("HandwritingRecognition/X.npy")
Y=np.load("HandwritingRecognition/Y.npy")
Y=np.reshape(Y,(-1,1))

onehotencoder = OneHotEncoder()

Y_ = onehotencoder.fit_transform(Y).toarray()

Y_=np.reshape(Y_,(3410,1,62))

model = keras.Sequential()

model.add(Bidirectional(LSTM(units=150), input_shape=(365, 2)))
model.add(RepeatVector(1))
model.add(Bidirectional(LSTM(units=150, return_sequences=True)))
model.add(Dense(units=62, activation='softmax'))
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

print(model.summary())

model.fit(X,Y_,batch_size=16,epochs=5,steps_per_epoch=214,validation_split=0.2)