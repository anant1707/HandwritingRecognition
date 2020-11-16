import os
import numpy as np
import xml.etree.ElementTree as ET


def parse():
    for dir in os.listdir('IAM/lineStrokes'):
    #ENTER NEW DIRECTORY-- eg: a01
        
        for subdir in os.listdir(f'IAM/lineStrokes/{dir}'):
        #ENTER NEW SUB-DIRECTORY-- eg: a01-000
            
            line_ascii=[]
            for filename in os.listdir(f'IAM/lineStrokes/{dir}/{subdir}'):
            #ENTER NEW FILE-- eg: a01-000U-01.XML
                if(filename.endswith('.xml')):
                    line_points=[]
                    
                    name=filename.split('.')[0]
                    line_number=int(name[-2:])
                    name=name[:-3]
                    
                    if(line_number==1):
                        file=open(f"IAM/ascii/{dir}/{subdir}/{name}.txt")
                        data=file.read()
                        data=data.split('CSR:')[-1]
                        data=data.split('\n')
                        line_ascii=[i for i in data if i!='']
                    
                    tree = ET.parse(f'IAM/lineStrokes/{dir}/{subdir}/{filename}')
                    root = tree.getroot()
        
                    for stroke in root.find('StrokeSet'):
                    #ENTER NEW STROKE-- eg: <Stroke></Stroke>
        
                        for point in stroke.findall('Point'):
                        #ENTER NEW POINT-- eg: <Point>
        
                            line_points.append((float(point.attrib['x']),float(point.attrib['y'])))
                    
                    line_points=[line_points,list(line_ascii[line_number-1])]
                    line_points=np.array(line_points)
                    np.save(f"IAM/lineStrokes/{dir}/{subdir}/{filename.split('.')[0]}.npy",line_points)
                    #print(filename)
        print(dir)



parse()

