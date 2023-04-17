from ast import main
from datetime import datetime
from genericpath import exists
import cv2, random, os
import numpy as np

os.chdir(r'D:\iec_ptit_2022\cvanomaly_detection\record')
os.listdir()
fol = ''
image_out_fol = "converted_image_data_set/"
input_fol = "image_data_set/"
inputPath = fol+input_fol
date = str(datetime.now()).split(' ')[0]
listDateFol = os.listdir(image_out_fol)
def make_folder(path):
    if(os.path.exists(path) == False):
        os.makedirs(path)
    return path

def check_file_exist(path):
    for d in listDateFol:
        # print(image_out_fol+d+'/'+path)
        if(os.path.exists(image_out_fol+d+'/'+path)):
            return True
    return False

for i in os.listdir(inputPath)[:]:
        j = '12-29-2022'
        for k in os.listdir(inputPath + i + "/" + j)[:]: 
            for l in  os.listdir(inputPath + i + "/" + j + "/" + k)[:]:
                if(not check_file_exist(i+"/" + l.split('.')[0] +'-'+ i + '.jpg')):
                    img = cv2.imread(inputPath + i + "/"  + j + "/" + k + "/" + l)
                    width = 1280
                    height = 720
                    dim = (width, height)
                    # resize image
                    img = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
                    cv2.imwrite(make_folder(image_out_fol+ date +'/') + l.split('.')[0] +'-'+ i + '.jpg',img)
                    print('convert img:' + l.split('.')[0] + '.jpg'+  '')
                else: print('ignore existed img:' + l.split('.')[0] + '.jpg')
print('convert done!')