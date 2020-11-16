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
model=keras.models.load_model("DL-part/Model/model_char74k.h5")
app = Flask(__name__)

#=============================================================================
#MYSQL CONFIGURATION
app.config['SECRET_KEY'] = 'AjJ0lXaX5K9tai8QsUhwwQ'


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


        if(len(StrokeSet)<365):
            StrokeSet=np.vstack((StrokeSet,(np.zeros((365-len(StrokeSet),2)))))

        #print(StrokeSet.shape)
        StrokeSet=np.reshape(StrokeSet,(1,365,2))


        char_map=[i for i in range(10)]

        AtoZ=list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
        atoz=list("abcdefghijklmnopqrstuvwxyz")
        char_map.extend(AtoZ)
        char_map.extend(atoz)

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
    app.run(host='127.0.0.1', port=5000, debug=True)