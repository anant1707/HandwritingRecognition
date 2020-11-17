# -- coding: utf-8 --
"""
Created on Mon Nov 16 15:35:58 2020

@author: Anant
"""
import numpy as np
import math

file=open(r"Data/UJI/ujipenchars2.txt",mode='r',encoding='utf-8')

def scale_down(x,fc):
    if(fc==True):
        skip=math.ceil(len(x)/(len(x)-120))
    else:
        skip=len(x)//(len(x)-120)
    templst=[]
    for i in range(len(x)):
        if(i%skip!=0):
            templst.append(x[i])
    return templst
def scale_up(x):
	templist=[]
	for i in range(len(x)-1):
		templist.append(x[i])
		templist.append(tuple((x[i][0]+x[i+1][0])/2,(x[i][1]+x[i+1][1])/2))
	templist.append(x[len(x)-1])
	return templist
def scale_up_prime(x):
	skip=math.ceil(len(x)/(120-len(x)))
	crnt=skip
	templst=[]
    for i in range(len(x)-1):
        templst.append(x[i])
        if(i==crnt):
        	templist.append(tuple((x[i][0]+x[i+1][0])/2,(x[i][1]+x[i+1][1])/2))
        	crnt+=skip

    templist.append(x[len(x)-1]) 
    return templst

nl=0
exc=['.', ',', ';',':', '?', '!', "'", '"', '(', ')', '%', '-', '@', '$', '<', '>']
X=[]
Y=[]
X_exc=[]
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
            
            if(len(x)>240):
                x=scale_down(x,True)
                
            if(len(x)>120):
                x=scale_down(x,False)
            if(len(x))>60:
            	x=scale_up_prime(x)
            if(len(x)<=60):
            	x=scale_up(x)
            if(len(x)<60):
            	x=scale_up(x)
            x=[x,char]
            #print(x)
            if char in exc:
                X_exc.append(x)
                continue
            X.append(x)
    else:
        pass

print("Done")


arr=np.array(X)

size=[]

for row in arr:
    size.append(len(row[0]))
    
size=sorted(list(set(size)),reverse=True)

np.save()