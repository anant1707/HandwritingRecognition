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
model=keras.models.load_model("DL-part/Model/model_74k_140.h5")
from bezier import evaluate_bezier
from math import ceil,floor,factorial
from sc import autocorrect
app = Flask(__name__)

#=============================================================================
#MYSQL CONFIGURATION
app.config['SECRET_KEY'] = 'AjJ0lXaX5K9tai8QsUhwwQ'


#HOMEPAGE

@app.route('/',methods=['GET','POST'])
def home():
	
    if(request.method=='POST'):
        resi=request.get_json(force=True)
        #print(res)
        #for a word
        char_strokes=[]
        prevmaxx=-1
        prevminx=1300
        # for a character
        prev_stroke_set=[]
        first=False
       #for a sentence
        line=[]
        
        for stroke in resi:
            lst=[]
            
            for c in stroke:
                  lst.append([float(c['x']),float(c['y'])])
                
            StrokeSet=np.array(lst)
        
        
            minx = min(StrokeSet[:, 0])
           
            maxx = max(StrokeSet[:, 0])
            
          
            if((minx<prevmaxx and minx>prevminx  ) or(maxx>prevminx and maxx<prevmaxx)or(minx<prevminx and maxx>prevmaxx) or (minx>prevminx and maxx<prevmaxx)or (minx<prevminx and maxx>prevmaxx)):
                
                prev_stroke_set.append(StrokeSet)
                prevmaxx=max(maxx,prevmaxx)
               
                
                prevminx=min(minx,prevminx)
            else:
                first=True
                
                diff=minx-prevmaxx-40
                print("Yippie")
                if(diff<0):
                    char_strokes.append(prev_stroke_set)
              
                    prev_stroke_set=[]
                    prev_stroke_set.append(StrokeSet)
                    prevmaxx=maxx
                    prevminx=minx
                else:
                    char_strokes.append(prev_stroke_set)
              
                    prev_stroke_set=[]
                    prev_stroke_set.append(StrokeSet)
                    prevmaxx=maxx
                    prevminx=minx
                    line.append(char_strokes)
                    char_strokes=[]
                    
                
                
        char_strokes.append(np.array(prev_stroke_set))
        line.append(char_strokes)
        char_strokes=0
        sentence=""
        for char_strokes in line:
            word=""
            
            for res in char_strokes:
                SS=[]
               
                for stroke in res:
                	lst=stroke
                	
                	SS.append(np.array(lst))
        
                sum=0
                sumi=0
                length=[]
                for i in SS:
                	length.append(len(i))
                	sum+=len(i)
        
                for i in range(len(length)):
                	length[i]=int((length[i]/sum)*140)
                	sumi+=length[i]
                sumi=sumi-length[-1]
        
                length[-1]=140-sumi
                print(length)
                for i in range(len(length)):
                	SS[i]= evaluate_bezier(SS[i],length[i])
        
                lst=SS[0]
                for i in range(len(length)-1):
                 	lst=np.vstack((lst,SS[i+1]))
                
                StrokeSet=lst
        
                x,y=StrokeSet[:,0],StrokeSet[:,1]
        
                
                minx = min(StrokeSet[:, 0])
                miny = min(StrokeSet[:, 1])
                maxx = max(StrokeSet[:, 0])
                maxy = max(StrokeSet[:, 1])
                StrokeSet[:, 0] = StrokeSet[:, 0] - minx
                StrokeSet[:, 1] = StrokeSet[:, 1] - miny
    
                StrokeSet[:, 0] = StrokeSet[:, 0] / (maxx-minx)
                StrokeSet[:, 1] = StrokeSet[:, 1] / (maxy-miny)
    
    
           
                print(StrokeSet.shape)
                StrokeSet=np.reshape(StrokeSet,(1,140,2))
    
    
    
                char_map=['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
               'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
               'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
               'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z','0','1','2','3','4','5','6','7','8','9']
    
            # x,y=StrokeSet[:,0],StrokeSet[:,1]
            # print("plotting started")
            # plt.plot(x, y, 'r.')
            # #plt.axis([0,1,1,0])
            # plt.savefig('plot.png')
            # plt.close()
            # print("plotting done")
            # # #print(StrokeSet)
                y=model.predict(StrokeSet)
                y=model.predict(StrokeSet)
    
                y=np.array(y)
                y=np.reshape(y,(62,))
                print(y[np.argmax(y)]*100)
                word+=str(char_map[np.argmax(y)])	
            print(word)
            sentence+=autocorrect(word)
            sentence+=' '
            
        return (sentence)
        
        
    return render_template('whiteboard.html',title='Home',character='default')

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
        

        for i in points:
            x.append((i[0]-minx)/(maxx-minx))
            y.append((i[1]-miny)/(maxy-miny))
        #print(x,y)

        plt.scatter(x,y)
        plt.axis([0,1,1,0])
        plt.savefig('plot.png')
        plt.close()

    return render_template('index.html',title='Home',character='default')



if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5001, debug=True)