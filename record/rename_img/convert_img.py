import cv2, random, os
from cv2 import resize
import numpy as np


os.chdir(r'D:\iec_ptit_2022\cvanomaly_detection\rename_image')
os.listdir()
fol = ''
frame_fol = fol + 'frame/'
VOC_anno_fol = fol + 'VOC_anno/'
house_fol = fol + 'house/preprocessed/'

image_out_fol = "img_out/"
input_fol = "img test/"
date_fol = "05-29-2022/"
preset_fol = "preset0/"
file_name = ""

def make_folder(path):
    if(os.path.exists(path) == False):
        os.makedirs(path)
    return path


# Create a VideoCapture object
print(fol + input_fol + file_name)

inputPath = fol+input_fol
c = 31
for i in os.listdir(inputPath)[:]:
    img = cv2.imread(inputPath + i )
    width = 1280
    height = 720
    dim = (width, height)
    # resize image
    img = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
    cv2.imwrite(make_folder(image_out_fol) + 'image' + str(c) + '.jpg',img)
    c+=1
    # print(inputPath + i + "/"  + j + "/" + k + "/" + l)
# img = cv2.imread(r'vacantland\vlcsnap-2022-09-08-12h56m30s878.png')
# width = 1280
# height = 720
# dim = (width, height)
# # resize image
# img = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
# cv2.imwrite('vlcsnap-2022-09-08-12h56m30s878.jpg',img)
#

#print(dist_list)
# matplotlib histogram
# plt.hist(dist_list, color = 'blue', edgecolor = 'black',
#          bins = int(50/5))

# # seaborn histogram
# sns.distplot(dist_list, hist=True, kde=False, 
#              bins=int(180/5), color = 'blue',
#              hist_kws={'edgecolor':'black'})
# # Add labels
# plt.title('Histogram of Arrival Delays')
# plt.xlabel('Delay (min)')
# plt.ylabel('Flights')
# plt.show()



# # Convert BGR to HSV
# hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
# # define range of a color in HSV
# lower_hue, upper_hue = color_seg(chosen_color)
# # Threshold the HSV image to get only blue colors
# mask = cv2.inRange(hsv, lower_hue, upper_hue)
#print(mask)

# cv2.imshow('frame',frame)
# cv2.imshow('mask',mask)

# cv2.waitKey(0)