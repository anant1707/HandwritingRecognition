# -*- coding: utf-8 -*-
"""
Created on Wed Nov 11 21:16:26 2020

@author: Anant
"""
import numpy as np
import os


def padd(x,maxlen):
    if(len(x)<maxlen):
        x=np.vstack((x,(np.zeros((maxlen-len(x),2)))))
    return x
def pad_dataset(X,maxlen):
    for i in range(len(X)):
        X[i]=padd(X[i],maxlen)
    return X
    
def load_dataset():
    X=[]
    Y=[]
    maxi=-1
    for dir in os.listdir("DATA/Char74k/Strokes"):
        if(dir.endswith('-new')):
            for files in os.listdir(f"DATA/Char74k/Strokes/{dir}"):
               arr= np.load(f"DATA/Char74k/Strokes/{dir}/{files}",allow_pickle=True)
               x=arr[0]
               y=arr[1]
               X.append(x)
               maxi=max(maxi,len(x))
               Y.append(y)
    X=pad_dataset(X,maxi)
    return np.array(X),np.array(Y),maxi


X_,Y_,ma=(load_dataset())
np.save("X.npy",X_)
np.save("Y.npy",Y_)


print(X_.shape,Y_.shape)

