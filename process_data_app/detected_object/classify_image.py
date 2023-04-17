# example of zoom image augmentation
import os
import shutil
import cv2
import numpy as np
import json
from pascal_voc_writer import Writer
fol =''
src_image_fol = fol + "detected_object/clips/"
label_fol = fol + "detected_object/labels/"


def make_folder(path):
    if(os.path.exists(path) == False):
        os.makedirs(path)
    return path

def get_polygon_of_img(img_name):
    bbox_file_name = img_name.replace('.jpg','.txt')

    f = open(label_fol+bbox_file_name)
    data = json.load(f)
    bbox = data['before']['box']
    after_bbox = data['after']['box']
    label = data['after']['label']
    bbox = np.reshape(after_bbox,(-1,2),order='A')
    
    return  label,bbox

def resize_img(img, polygon):
    original_width, original_height = img.shape[1], img.shape[0]
    resized_width = 1280
    resized_height = 720
    resized_img = cv2.resize(img,(resized_width,resized_height))
    for i in range(len(polygon)):
        polygon[i,0] =int(polygon[i,0]*resized_width/(original_width))
        polygon[i,1] =int(polygon[i,1]* resized_height/(original_height))
    return resized_img, polygon

def copy_and_overwrite(from_path, to_path):
    if not os.path.exists(to_path):
        shutil.copy(from_path, to_path)

def process_each_data(img_name,verify):
    label, polygon = get_polygon_of_img(img_name)
    img_rename = img_name.replace('.jpg','-clean.png')
    img = cv2.imread(src_image_fol + img_rename)    
    img_rename = img_rename.replace('.png','.jpg')
    resized_img, polygon = resize_img(img, polygon)
    if(verify == 0):
        label = 'not' + label
        
    cv2.imwrite(make_folder('detected_object/output_data/images/')+img_rename,resized_img)
    writer = Writer('images/'+img_rename, resized_img.shape[1], resized_img.shape[0])
    # add objects (class, xmin, ymin, xmax, ymax)
    writer.addObject(label, polygon[0][0], polygon[0][1], polygon[1][0], polygon[1][1])
    # write to file
    writer.save(make_folder('detected_object/output_data/annotations/xmls/') + img_rename.replace('.jpg','.xml'))
#main
def process_data():
    f = open('detected_object/verified_img_list.txt')
    data = f.read()
    lines  = data.splitlines()
    lines  = [line.split(' ') for line in lines]
    img_list = [(img,int(ver)) for img,ver in lines]
    return img_list
    # for img_name,verify in img_list: 
    #     process_each_data(img_name,verify)
            
    
