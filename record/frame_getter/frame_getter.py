import datetime
import time
import cv2, random, os
import numpy as np
import sys
#import matplotlib.pyplot as plt

os.chdir(r'D:\iec_ptit_2022\cvanomaly_detection\frame_getter')
os.listdir()

fol = ''
frame_fol = fol + 'frame/'
VOC_anno_fol = fol + 'VOC_anno/'
input_fol = fol + 'video_data_set/'
# Create a VideoCapture object
c = 0
start_time = sys.argv[0]
end_time = sys.argv[1]

def make_folder(path):
    if(os.path.exists(path) == False):
        os.makedirs(path)
    return path

def time_to_secs(t):
    x = time.strptime(t,'%H:%M:%S')
    return datetime.timedelta(hours=x.tm_hour,minutes=x.tm_min,seconds=x.tm_sec).total_seconds()
def main():
    start_time = sys.argv[1]
    end_time = sys.argv[2]
    for i in os.listdir(input_fol):
        frame_fol = fol + i.split('.')[0]+'/'
        cap = cv2.VideoCapture(input_fol + i)
        frame_count =  cap.get(cv2.CAP_PROP_FRAME_COUNT)
        frame_rate = cap.get(cv2.CAP_PROP_FPS)
        # print(frame_count,frame_rate)
        start_frame = int(time_to_secs(start_time)*frame_rate)
        end_frame =  int(time_to_secs(end_time)*frame_rate)
        print('extract frame from ' + i + '\n start time: ' + start_time + '\n end time: ' + end_time + '\n total frame: ' + str(end_frame-start_frame) )

        # print(end_frame)
        cap.set(cv2.CAP_PROP_POS_FRAMES,time_to_secs(start_time)*frame_rate)
        # print(cap.get(cv2.CAP_PROP_POS_FRAMES))
        # Check if camera opened successfully
        if (cap.isOpened() == False): 
            print("Unable to read camera feed")
        # Default resolutions of the frame are obtained.The default resolutions are system dependent.
        # We convert the resolutions from float to integer.
        frame_width = int(cap.get(3))
        frame_height = int(cap.get(4))    
        while(cap.get(cv2.CAP_PROP_POS_FRAMES)<= end_frame):
            ret, frame = cap.read()
            if ret == True: 
                width = 1280
                height = 720
                dim = (width, height)
                # resize image
                frame = cv2.resize(frame, dim, interpolation = cv2.INTER_AREA)
                cv2.imwrite(make_folder(frame_fol) + 'frame_'+ i.split('.')[0]+'_' + str(int(cap.get(cv2.CAP_PROP_POS_FRAMES))) + '.jpg', frame)
                print(' extract frame ' + str(cap.get(cv2.CAP_PROP_POS_FRAMES)))
            #   break
        # Break the loop
            else:
                break  
        # When everything done, release the video capture and video write objects
        cap.release()
        # Closes all the frames
        cv2.destroyAllWindows()
        print('Done!')
if __name__ == '__main__':
    main()