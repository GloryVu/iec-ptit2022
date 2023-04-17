import shutil
import cv2, os
import numpy as np
from preprocess_data.trimap_module import trimap,extractImage
from glob import glob
src_imgs = 'detected_object/output_data/images/'
src_trimaps = 'detected_object/output_data/annotations/trimaps/'
def make_folder(path):
    if(os.path.exists(path) == False):
        os.makedirs(path)
    return path

def get_list_file():
    list = os.listdir(src_imgs)
    processed = os.listdir(src_trimaps)
    processed = [img.replace('.png','.jpg') for img in processed]
    return [img for img in list if img not in processed]

def process_each_trimap(file_name):
    # try:
    path = src_imgs+file_name
    # print(path)
    image   = extractImage(path)
    # print(image)
    name    = file_name.split('.jpg')[0]
    size    = 30; # how many pixel extension do you want to dilate
    number  = 1;  # numbering purpose 
    if os.path.exists(src_trimaps+name+'.png'):
        return
    trimap_name,trimap_img = trimap(image, name, size, number, erosion=False)
    cv2.imwrite(make_folder(src_trimaps)+trimap_name,trimap_img)
    # except Exception as e:
    #     print(e)


