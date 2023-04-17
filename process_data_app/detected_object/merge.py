from glob import glob
from itertools import count
import random
import os
import shutil

def append_txt_file(firstfile,secondfile):
    # opening first file in append mode and second file in read mode
    if(not os.path.exists(firstfile)):
        f1 = open(firstfile,'w')
        f1.close()
    f1 = open(firstfile, 'a+')
    f2 = open(secondfile, 'r')

    # appending the contents of the second file to the first file
    f1.write(f2.read())

    # closing the files
    f1.close()
    f2.close()


paths = [r'D:\iec_ptit_2022\cvanomaly_detection\detected_object\not_foundationhouse',
        r'D:\iec_ptit_2022\cvanomaly_detection\detected_object\not_smoke',
        r'D:\iec_ptit_2022\cvanomaly_detection\detected_object\not_vacantland'
        ]
dst_path = r'D:\iec_ptit_2022\cvanomaly_detection\detected_object\merge'
os.chdir(dst_path)
if(os.path.exists(dst_path+r'\annotations')):
    shutil.rmtree(dst_path+r'\annotations')        
os.makedirs(dst_path+r'\annotations')

if(os.path.exists(dst_path+r'\annotations\tripmaps')):
    shutil.rmtree(dst_path+r'\annotations\trimaps')
os.makedirs(dst_path+r'\annotations\trimaps')    

if(os.path.exists(dst_path+r'\annotations\xmls')):
    shutil.rmtree(dst_path+r'\annotations\xmls')
os.makedirs(dst_path+r'\annotations\xmls')  
        
if(os.path.exists(dst_path+r'\images')):
    shutil.rmtree(dst_path+r'\images')
os.makedirs(dst_path+r'\images')  
for i in paths:
    #copy images
    list_file = glob(i+"//images//*")
    for file_path in list_file:
        name_file = file_path.split('\\')[-1]
        src = file_path
        dst = dst_path+r'\images'+'/'+name_file
        shutil.copy(src,dst)
    #copy trimaps
    list_file = glob(i+"//trimaps//*")
    for file_path in list_file:
        name_file = file_path.split('\\')[-1]
        src = file_path
        dst = dst_path+r'\annotations\trimaps'+'/'+name_file
        shutil.copy(src,dst)
    #copy trimaps
    list_file = glob(i+"//xmls//*")
    for file_path in list_file:
        name_file = file_path.split('\\')[-1]
        src = file_path
        dst = dst_path+r'\annotations\xmls'+'/'+name_file
        shutil.copy(src,dst)
    #append list
    append_txt_file(dst_path+'/annotations/list.txt',i+'/list.txt')
     
    #append test
    append_txt_file(dst_path+'/annotations/test.txt',i+'/test.txt')
    
    #append list
    append_txt_file(dst_path+'/annotations/trainval.txt',i+'/trainval.txt')   