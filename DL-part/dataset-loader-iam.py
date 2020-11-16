import numpy as np

def padd_X(x,maxlen):
    if(len(x)<maxlen):
        x=np.vstack((x,(np.zeros((maxlen-len(x),2)))))
    return x

def pad_X(X,maxlen):
    for i in range(len(X)):
        X[i]=padd_X(X[i],maxlen)
    return X
    
def load_dataset():
    X=[]
    Y=[]
    maxi=-1

                
    arr= np.load(f"Data/UJI/raw-data.npy",allow_pickle=True)
    for row in arr:
        

        x=np.array(row[0])
        y=row[1]
        #print(y)
        
        minx = min(x[:, 0])
        miny = min(x[:, 1])
        maxx = max(x[:, 0])
        maxy = max(x[:, 1])
        
        x[:, 0] = x[:, 0] - minx
        x[:, 1] = x[:, 1] - miny
        
        
        if(minx==maxx):
            continue
        if(miny==maxy):
            continue
        
        x[:, 0] = x[:, 0] / (maxx-minx)
        x[:, 1] = x[:, 1] / (maxy-miny)

        
        
        X.append(x)
        
        maxi=max(maxi,len(x))

        Y.append(y)

                    
    return X,Y,maxi
                    


X_,Y_,ma=(load_dataset())

X=np.array(pad_X(X_, ma))
Y=np.array(Y_)

char_map=(list(Y[:78*2-1]))
char_map=[char_map[i] for i in range (0,len(char_map),2)]

yy=[]
for char in Y:
    yy.append(char_map.index(char)+1)
Y=np.array(yy)

print(X.shape,Y.shape)



