# -- coding: utf-8 --
"""
Created on Mon Nov 16 15:35:58 2020

@author: Anant
"""
import math


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
		templist.append(((x[i][0]+x[i+1][0])/2,(x[i][1]+x[i+1][1])/2))
	templist.append(x[len(x)-1])
	return templist
def scale_up_prime(x):
    skip=math.ceil(len(x)/(120-len(x)))
    crnt=skip
    templst=[]
    for i in range(len(x)-1):
        templst.append(x[i])
        if(i==crnt):
        	templst.append(((x[i][0]+x[i+1][0])/2,(x[i][1]+x[i+1][1])/2))
        	crnt+=skip

    templst.append(x[len(x)-1]) 
    return templst
