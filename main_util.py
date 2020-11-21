@app.route('/letter',methods=['GET','POST'])
def letter():
    if(request.method=='POST'):
        res=request.get_json(force=True)

        SS=[]

        for stroke in res:
        	lst=[]
        	for c in stroke:
        		lst.append([float(c['x']),float(c['y'])])
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


       
        xx,yy=StrokeSet[:,0],StrokeSet[:,1]
        StrokeSet=np.reshape(StrokeSet,(1,140,2))


        
        print("plotting started")
        plt.plot(xx, yy, 'r')
        plt.axis([0,1,1,0])
        plt.savefig('plot.png')
        plt.close()
        print("plotting done")
        # # #print(StrokeSet)
        y=model.predict(StrokeSet)

        y=np.array(y)
        y=y[0]
       	
        y=np.dstack((y,ii))
        y=y[0].tolist()
        y=sorted(y,reverse=True)
        
        output=""
        for i in range(3):
        	output+=str(char_map[int(y[i][1])])
        	output+=" "
        return output, 200
        
        
    return render_template('index.html',title='Home',character='default')

@app.route('/word',methods=['GET','POST'])
def word():
	if(request.method=='POST'):
		resi=request.get_json(force=True)
		#print(res)
		char_strokes=[]
		prevmaxx=-1
		prevminx=1300
		prev_stroke_set=[]
		first=False


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
				char_strokes.append(prev_stroke_set)

				prev_stroke_set=[]
				prev_stroke_set.append(StrokeSet)
				prevmaxx=maxx
				prevminx=minx
                
                
		char_strokes.append(prev_stroke_set)
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

			StrokeSet=np.reshape(StrokeSet,(1,140,2))
			y=model.predict(StrokeSet)
			y=np.array(y)
			y=y[0]

			y=np.dstack((y,ii))
			y=y[0].tolist()
			y=sorted(y,reverse=True)

			word+=char_map[int(y[0][1])]
			if(y[0][0]>0.9):
				print(show_first(y,1))
			else:
				print(show_first(y,2))
		return (word)
        
        
	return render_template('index.html',title='Home',character='default')
   # 90+  1
           # 75-90 2
           # 50+ 3
           # <50 4

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
            x.append((i-minx)/(maxx-minx))
            y.append(0.5)
        #print(x,y)

        plt.scatter(x,y)
        plt.axis([0,1,1,0])
        plt.savefig('plot.png')
        plt.close()

    return render_template('index.html',title='Home',character='default')
