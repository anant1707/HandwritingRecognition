# -*- coding: utf-8 -*-
"""
Created on Wed Nov 11 22:50:56 2020

@author: Anant
"""

import keras
import numpy as np
import random
model=keras.models.load_model("Model/model_new.h5")


f= open("cord.txt",'r')
def cnvt(t):
    if(t[0].endswith(',') ):
        t[0]=t[0][:-1]
    if(t[1].endswith(',') ):
        t[1]=t[1][:-1]
    return (float(t[0]),float(t[1]))
data = f.read().split("\n")

lst=[i.split('{')[1][3:14].split(', y:') for i in data]
lst=(list(map(cnvt,lst)))

StrokeSet=np.array(lst)
#print(lst)

#StrokeSet=np.reshape(lst,(1,-1,2))
minx = min(StrokeSet[:, 0])
miny = min(StrokeSet[:, 1])
maxx = max(StrokeSet[:, 0])
maxy = max(StrokeSet[:, 1])

#print(minx,miny,maxx,maxy)

StrokeSet[:, 0] = StrokeSet[:, 0] - minx
StrokeSet[:, 1] = StrokeSet[:, 1] - miny

StrokeSet[:, 0] = StrokeSet[:, 0] / (maxx-minx)
StrokeSet[:, 1] = StrokeSet[:, 1] / (maxy-miny)


if(len(StrokeSet)<365):
    StrokeSet=np.vstack((StrokeSet,(np.zeros((365-len(StrokeSet),2)))))

#print(StrokeSet.shape)
StrokeSet=np.reshape(StrokeSet,(1,365,2))


char_map=[i for i in range(10)]

AtoZ=list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
atoz=list("abcdefghijklmnopqrstuvwxyz")
char_map.extend(AtoZ)
char_map.extend(atoz)

y=model.predict(StrokeSet)

y=np.array(y)
y=np.reshape(y,(62,))
print(char_map[np.argmax(y)],y[np.argmax(y)]*100)
