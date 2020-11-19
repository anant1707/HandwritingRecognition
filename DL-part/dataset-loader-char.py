# -*- coding: utf-8 -*-
"""
Created on Wed Nov 11 21:16:26 2020

@author: Anant
"""
import numpy as np
import os
char_map_74k=[str(i) for i in range(10)]

AtoZ=list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
atoz=list("abcdefghijklmnopqrstuvwxyz")
char_map_74k.extend(AtoZ)
char_map_74k.extend(atoz)

char_map=['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
           'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
           'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
           'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z','0','1','2','3','4','5','6','7','8','9']
def load_dataset():
    X=[]
    Y=[]
    maxi=-1
    for dir in os.listdir("Data/Char74k/Strokes"):
        if(dir.endswith('-new')):
            for files in os.listdir(f"Data/Char74k/Strokes/{dir}"):
               arr= np.load(f"Data/Char74k/Strokes/{dir}/{files}",allow_pickle=True)
               x=arr[0]
               y=arr[1]
               X.append(x)
               Y.append(y)
    #X=pad_dataset(X,maxi)
    return np.array(X),np.array(Y),maxi


X_,Y_,ma=(load_dataset())
np.save("Data/Char74k/X.npy",X_)
np.save("Data/Char74k/Y.npy",Y_)


print(X_.shape,Y_.shape)


