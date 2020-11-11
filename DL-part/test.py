# -*- coding: utf-8 -*-
"""
Created on Wed Nov 11 22:50:56 2020

@author: Anant
"""

import keras
import numpy as np
import random
model=keras.models.load_model("HandwritingRecognition/model.h5")

X=np.load("HandwritingRecognition/X.npy")
Y=np.load("HandwritingRecognition/Y.npy")

f= open("HandwritingRecognition/cord.txt",'r')
def cnvt(t):
    if(t[0].endswith(',') ):
        t[0]=t[0][:-1]
    if(t[1].endswith(',') ):
        t[1]=t[1][:-1]
    return (float(t[0])/1200,float(t[1])/900)
data = f.read().split("\n")

lst=[i.split('{')[1][3:14].split(', y:') for i in data]
lst=(list(map(cnvt,lst)))
if(len(lst)<365):
    for i in range(365-len(lst)):
        lst.append((0,0))
lst=np.array(lst)
print(lst)



x=np.reshape(lst,(1,365,2))
print(x)
y=model.predict(x)

print(Y[1156])


