# -*- coding: utf-8 -*-
"""
Created on Thu Nov 12 20:35:51 2020

@author: Anant
"""
import os
from flask import Flask, render_template, request, jsonify
import keras
import numpy as np
import random
import matplotlib.pyplot as plt
model=keras.models.load_model("DL-part/Model/model_UJI2_newest.h5")

app = Flask(__name__)

#=============================================================================
#MYSQL CONFIGURATION
app.config['SECRET_KEY'] = 'AjJ0lXaX5K9tai8QsUhwwQ'

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
#HOMEPAGE

@app.route('/',methods=['GET','POST'])
def home():
    if(request.method=='POST'):
        res=request.get_json(force=True)
        #print(res)
        lst=[]
        for stroke in res:
            for c in stroke:
                lst.append((float(c['x']),float(c['y'])))
        
        #print(lst)

        if(len(lst)>240):
            lst=scale_down(lst,True)
                
        if(len(lst)>120):
            lst=scale_down(lst,False)
        

        StrokeSet=np.array(lst)
        
        #print(StrokeSet)
        minx = min(StrokeSet[:, 0])
        miny = min(StrokeSet[:, 1])
        maxx = max(StrokeSet[:, 0])
        maxy = max(StrokeSet[:, 1])

        #print(minx,miny,maxx,maxy)

        StrokeSet[:, 0] = StrokeSet[:, 0] - minx
        StrokeSet[:, 1] = StrokeSet[:, 1] - miny

        StrokeSet[:, 0] = StrokeSet[:, 0] / (maxx-minx)
        StrokeSet[:, 1] = StrokeSet[:, 1] / (maxy-miny)


        if(len(StrokeSet)<120):
            StrokeSet=np.vstack((StrokeSet,(np.zeros((120-len(StrokeSet),2)))))

        #print(StrokeSet.shape)
        StrokeSet=np.reshape(StrokeSet,(1,120,2))


        char_map=['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
       'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
       'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
       'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z',
       '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

        #print(StrokeSet)
        y=model.predict(StrokeSet)

        y=np.array(y)
        y=np.reshape(y,(62,))

        #print(y[np.argmax(y)]*100)
        return (str(char_map[np.argmax(y)])+str(y[np.argmax(y)]*100)), 200
        
        
    return render_template('index.html',title='Home',character='default')

@app.route('/plot',methods=['GET','POST'])
def plot():
    if(request.method=='POST'):
        res=request.get_json(force=True)
        
        points=[]
        for stroke in res:
            for c in stroke:
                points.append((float(c['x']),float(c['y'])))

        StrokeSet=np.array(points)
        #print(StrokeSet)
        minx = min(StrokeSet[:, 0])
        miny = min(StrokeSet[:, 1])
        maxx = max(StrokeSet[:, 0])
        maxy = max(StrokeSet[:, 1])

        #print(minx,miny,maxx,maxy)

        points=sorted(points)
        # print(points)
        x=[]
        y=[]
        dictionary={}
        for c in points:
            if(c[0] in dictionary):
                dictionary[c[0]]=min(dictionary[c[0]],c[1])
            else:
                dictionary[c[0]]=c[1]

        for i in sorted(dictionary.keys()):
            x.append(i-minx)
            y.append(dictionary[i]-miny)
        #print(x,y)

        plt.plot(x,y,'-ro')
        plt.axis([-10,maxx-minx+10,maxy-miny+10,-10])
        plt.savefig('plot.png')
        plt.close()

    return render_template('index.html',title='Home',character='default')



if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5001, debug=True)