# -*- coding: utf-8 -*-
"""
Created on Mon Nov 16 15:35:58 2020

@author: Anant
"""
import numpy as np

file=open(r"Data/UJI/ujipenchars2.txt",mode='r',encoding='utf-8')

nl=0

X=[]
Y=[]
for temp in file:
    if temp.startswith('// A'):
        for k in range(2):
            temp=file.readline()
            char=temp.split(' ')[1]
            ns=int(file.readline().split(' ')[-1])
            x=[]
            for i in range(ns):
                point=file.readline().split('#')[-1]
                point=point.split('\n')[0].split(' ')
                point.pop(0)
                for i in range(0,len(point),2):
                    x.append((float(point[i]),float(point[i+1])))
                
            x=[x,char]
            #print(x)
            X.append(x)
    else:
        pass

print("Done")



arr=np.load("Data/UJI/X.npy",allow_pickle=True)