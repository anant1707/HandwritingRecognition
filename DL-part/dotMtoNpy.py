import os
import numpy as np
def cnvt(t):
    return (float(t[0])/1200,float(t[1])/900)
def parse(path,code):
    with open(path) as file:
        data = file.read().replace('e+002\n', 'e+002,')
        data = data.replace('e+001\n', 'e+001,')
        data = data.replace('e+003\n', 'e+003,')
        
    r,c,_=data.split('};')
    r=r.split('{')[-1]
    c=c.split('{')[-1]
    r=r.replace(',];', '];')
    c=c.replace(',];', '];')
    
    r=r.split(';\n')
    c=c.split(';\n')
    
    r.pop(-1)
    c.pop(-1)
    
    row=[]
    col=[]
    
    for rr in r:
        row.append(rr[1:-1].split(','))
        
    for cc in c:
        col.append(cc[1:-1].split(','))
    
    tempStrokeSet=[]
    for i in range(len(row)):
        tempStrokeSet.extend(list(zip(col[i],row[i])))
    

    StrokeSet=np.array(list(map(cnvt,tempStrokeSet)))
    StrokeSet=[StrokeSet,code]

    return np.array(StrokeSet)



for dir in os.listdir("DATA/Char74k/Strokes"):
    if(not(dir.endswith('-new'))):
        for files in os.listdir(f"DATA/Char74k/Strokes/{dir}"):
            np.save(f"DATA/Char74k/Strokes/{dir}-new/{files.split('.')[0]}.npy",parse(f"DATA/Char74k/Strokes/{dir}/{files}",int(dir[6:])))
        

