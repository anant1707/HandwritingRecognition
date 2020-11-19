# -- coding: utf-8 --
"""
Created on Mon Nov 16 15:35:58 2020

@author: Anant
"""
import numpy as np

import matplotlib.pyplot as plt
from math import factorial,floor

def comb(n, k):
    return factorial(n) // (factorial(k) * factorial(n - k))

def get_bezier_curve(points):
    n = len(points) - 1
    return lambda t: sum(
        comb(n, i) * t**i * (1 - t)**(n - i) * points[i]
        for i in range(n + 1)
    )

def evaluate_bezier(points, total):
    bezier = get_bezier_curve(points)
    new_points = np.array([bezier(t) for t in np.linspace(0, 1, total)])
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
            point=0
            points=[]
            length=[]
            sumi=0
            for i in range(ns):
                point=file.readline().split('#')[-1]
                point=point.split('\n')[0].split(' ')
                point.pop(0)
                points.append(point)
                length.append(len(point)/2)
                sumi+=len(point)/2
            total=140/sumi
            sumi=0
            for i in range(ns):
                length[i]=floor(length[i]*total)
                sumi+=length[i]
            sumi-=length[-1]
            
            length[-1]=140-sumi
            x=[]
            for i in range(ns):
                stroke=[]
                point=points[i]
                for j in range(0,len(point),2):
                    stroke.append([float(point[j]),float(point[j+1])])
                
                stroke=np.array(stroke)
                
                stroke=evaluate_bezier(stroke, length[i])
                if(i==0):
                    x=stroke
                else:
                    x=np.vstack((x,stroke))
                
                 
                
          
            count+=1
            if(count%50==0):
                  print(f"Yippie ,{count/50}")
                 
                  
           
            x=[x,char]
            #print(x)
            if char in exc:
                X_exc.append(x)
                continue
            X.append(x)
    else:
        pass

print("Done")