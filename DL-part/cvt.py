# -*- coding: utf-8 -*-
"""
Created on Thu Nov 12 00:07:21 2020

@author: Anant
"""
import numpy as np
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

