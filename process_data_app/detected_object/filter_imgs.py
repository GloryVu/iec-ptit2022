# example of zoom image augmentation
import os
import shutil
os.chdir(r'D:\iec_ptit_2022\cvanomaly_detection\detected_object')
import cv2
import numpy as np
import json
from pascal_voc_writer import Writer
fol =''
src_image_fol = fol + "clips/"
label_fol = fol + "label/"


def make_folder(path):
    if(os.path.exists(path) == False):
        os.makedirs(path)
    return path

def copy_and_overwrite(from_path, to_path):
    if not os.path.exists(to_path):
        shutil.copy(from_path, to_path)

#main
# copy file 
src = r'D:\iec_ptit_2022\cvanomaly_detection\sharedwithVM\clips'
dest =r'D:\iec_ptit_2022\cvanomaly_detection\detected_object\clips'
for i in os.listdir(src):
    copy_and_overwrite(src+'/'+i,dest+'/'+i)

src = r'D:\iec_ptit_2022\cvanomaly_detection\sharedwithVM\labels'
dest =r'D:\iec_ptit_2022\cvanomaly_detection\detected_object\labels'
for i in os.listdir(src):
    copy_and_overwrite(src+'/'+i,dest+'/'+i)

for i in os.listdir(src_image_fol)[:]: #date
    if i.split('.')[2] == 'jpg':
        if os.path.exists(label_fol+i.replace('.jpg','.txt')):
            shutil.copy(src_image_fol+i,make_folder('bbox_image/')+i)
        continue

    
        
   
