import os
import numpy as np
import math

def cnvt(t):
    return [float(t[0]),float(t[1])]
def comb(n, k):
    return math.factorial(n) // (math.factorial(k) * math.factorial(n - k))

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


char_map_74k=[str(i) for i in range(10)]

AtoZ=list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
atoz=list("abcdefghijklmnopqrstuvwxyz")
char_map_74k.extend(AtoZ)
char_map_74k.extend(atoz)

char_map=['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
           'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
           'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
           'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z','0','1','2','3','4','5','6','7','8','9']

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
    
    tStrokeSet=[]
    for i in range(len(row)):
        tStrokeSet.append(list(zip(col[i],row[i])))
    
    SS=[]
    for stroke in tStrokeSet:
        SS.append(np.array(list(map(cnvt,stroke))))
    
    sum=0
    sumi=0
    length=[]
    for i in SS:
    	length.append(len(i))
    	sum+=len(i)

    for i in range(len(length)):
    	length[i]=int((length[i]/sum)*140)
    	sumi+=length[i]

    length[-1]+=(140-sumi)

    for i in range(len(length)):
    	SS[i]= evaluate_bezier(SS[i],int(math.floor(length[i])))

    lst=SS[0]
    for i in range(len(length)-1):
    	lst=np.vstack((lst,SS[i+1]))
    
    StrokeSet=lst


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
    
    StrokeSet=[StrokeSet,code]

    return StrokeSet


for dir in os.listdir("Data/Char74k/Strokes"):
    print(dir)
    if(not dir.endswith('-new')):
        for files in os.listdir(f"Data/Char74k/Strokes/{dir}"):
            np.save(f"Data/Char74k/Strokes/{dir}-new/{files.split('.m')[0]}.npy",parse(f"Data/Char74k/Strokes/{dir}/{files}",int(dir[6:])))
            
print("Done")

