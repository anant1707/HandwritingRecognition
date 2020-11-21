# -*- coding: utf-8 -*-
"""
Created on Thu Nov 19 20:13:43 2020

@author: Anant
"""
import numpy as np

X_74k=np.load("Data/Char74k/X.npy",allow_pickle=True)
Y_74k=np.load("Data/Char74k/Y.npy",allow_pickle=True)
X_uji=np.load("Data/UJI/X.npy",allow_pickle=True)
Y_uji=np.load("Data/UJI/Y.npy",allow_pickle=True)


X=np.vstack((X_74k,X_uji))
Y=np.hstack((Y_74k,Y_uji))