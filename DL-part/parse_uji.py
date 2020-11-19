# -- coding: utf-8 --
"""
Created on Mon Nov 16 15:35:58 2020

@author: Anant
"""
import numpy as np

import matplotlib.pyplot as plt
from math import factorial

def comb(n, k):
    return factorial(n) // (factorial(k) * factorial(n - k))

def get_bezier_curve(points):
    n = len(points) - 1
    return lambda t: sum(
        comb(n, i) * t*i * (1 - t)*(n - i) * points[i]
        for i in range(n + 1)
    )

def evaluate_bezier(points, total):
    bezier = get_bezier_curve(points)
    new_points = list([bezier(t) for t in np.linspace(0, 1, total)])
    return new_points




file=open(r"Data/UJI/ujipenchars2.txt",mode='r',encoding='utf-8')




nl=0
exc=['.', ',', ';',':', '?', '!', "'", '"', '(', ')', '%', '-', '@', '$', '<', '>']
X=[]
Y=[]
X_exc=[]
count=0
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
                    x.append([float(point[i]),float(point[i+1])])
                
            x=np.array(x)
            count+=1
            if(count%50==0):
             print(f"Yippie ,{count/50}")
            
            x= evaluate_bezier(x,140)
           # temp=np.array([250]*140)
           # plt.plot(bx, temp, 'b.')
            #plt.plot(x, [500]*29, 'r.')
            #plt.axis([0,1000,1000,0])
            #plt.show()
            x=[x,char]
            #print(x)
            if char in exc:
                X_exc.append(x)
                continue
            X.append(x)
    else:
        pass

print("Done")