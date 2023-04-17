from datetime import datetime
import schedule
import vlc
import time
import os
import threading
#["--demux=ts ]
camera_links = ["rtsp://iocldg:iocldg123123@10.1.20.4:554/profile1/media.smp",
"rtsp://iocldg:iocldg123123@10.1.20.16:554/profile1/media.smp",
"rtsp://iocldg:iocldg123123@10.1.20.14:554/profile1/media.smp",
"rtsp://iocldg:iocldg123123@10.1.20.15:554/profile1/media.smp",
"rtsp://iocldg:iocldg123123@10.1.20.18:554/profile1/media.smp",
"rtsp://iocldg:iocldg123123@10.1.20.19:554/profile1/media.smp",
"rtsp://iocldg:iocldg123123@10.1.20.10:554/profile1/media.smp",
"rtsp://iocldg:iocldg123123@10.1.20.24:554/profile1/media.smp",
"rtsp://iocldg:iocldg123123@10.1.20.25:554/profile1/media.smp",
"rtsp://iocldg:iocldg123123@10.1.20.26:554/profile1/media.smp",
"rtsp://iocldg:iocldg123123@10.1.20.29:554/profile1/media.smp",
"rtsp://iocldg:iocldg123123@10.1.20.30:554/profile1/media.smp",
"rtsp://iocldg:iocldg123123@10.1.20.12:554/profile1/media.smp",
"rtsp://iocldg:iocldg123123@10.1.20.20:554/profile1/media.smp",
"rtsp://iocldg:iocldg123123@10.1.20.21:554/profile1/media.smp",
"rtsp://iocldg:iocldg123123@10.1.20.22:554/profile1/media.smp",
"rtsp://iocldg:iocldg123123@10.1.20.6:554/profile1/media.smp",
"rtsp://iocldg:iocldg123123@10.1.20.17:554/profile1/media.smp",
"rtsp://iocldg:iocldg123123@10.1.20.5:554/profile1/media.smp",
"rtsp://iocldg:iocldg123123@10.1.20.23:554/profile1/media.smp",
"rtsp://iocldg:iocldg123123@10.1.20.27:554/profile1/media.smp",
"rtsp://iocldg:iocldg123123@10.1.20.28:554/profile1/media.smp"]
num_of_camera = 1
num_of_preset = 12

path = "D://iec_ptit_2022/cvanomaly_detection/record/image_data_set_test/"
presetName ="preset"
video_path = "D://iec_ptit_2022/cvanomaly_detection/record/video_data_set_test/"
#get Preset Path
def get_preset_path(iter,preset):
    dateFolder = datetime.now().strftime("%m-%d-%Y") + '/'
    presetPath = path + 'camera'+str(iter)+'/'+ dateFolder + presetName+str(preset)
    if(os.path.exists(presetPath) == False):
        os.makedirs(presetPath)
    return presetPath

def get_video_preset_path(iter):
    dateFolder = datetime.now().strftime("%m-%d-%Y") + '/'
    video_preset_path = video_path + 'camera'+str(iter)+'/' + dateFolder
    if(os.path.exists(video_preset_path) == False):
        os.makedirs(video_preset_path)
    return video_preset_path
vlcInstance = [vlc.Instance("--demux=ts",b"--rtsp-frame-buffer-size=800000",b"--network-caching=1000")]*num_of_camera
media_player_snapshot = [None]*num_of_camera
print(media_player_snapshot)

for i in range(num_of_camera):
    media_player_snapshot[i] = vlcInstance[0].media_player_new()
media_player_records  = [[None]*num_of_preset]*num_of_camera 
for i in range(num_of_camera):
    for j in range(num_of_preset):
        media_player_records[i][j] = vlcInstance[0].media_player_new()
    
media_snapshot = [None]*num_of_camera
for i in range(num_of_camera):
    media_snapshot[i] = vlcInstance[0].media_new(camera_links[i])
    mediaName ="camera_" +str(i) + "preset_" + datetime.now().strftime("%m-%d-%Y-%Hh%Mm%Ss") +".avi"
    media_snapshot[i].add_option("sout=#duplicate{dst=display,dst=standard{access=file,mux=avi,dst="+get_video_preset_path(i)+ "/" + mediaName+"}}")
#media_snapshot.get_mrl()
# setting media to the media player
for i in range(num_of_camera):
    media_player_snapshot[i].set_media(media_snapshot[i])
    
# setting video scale
for i in range(num_of_camera):
    media_player_snapshot[i].video_set_scale(0.1)  
# start playing video
for i in range(num_of_camera):
    media_player_snapshot[i].play()

#
is_preparing = [0]*22
is_reset = [False]*22
def reset_media_player_snapshot(iter):
    global is_reset
    global is_preparing
    if(media_player_snapshot[iter].is_playing() == 0 & is_reset[iter] == False):
        print("resetting stream")
        #global is_reset
        #global is_preparing
        is_reset[iter] = True
  
        #media_player_snapshot.release();
        while(media_player_snapshot[iter].is_playing() == 0):
            media_player_snapshot[iter].stop()
            media_player_snapshot[iter].play()
            time.sleep(1)
 
        is_preparing = 20
        while(is_preparing > 0):
            
            if(media_player_snapshot[iter].is_playing() == 0):
                is_preparing[iter] = -1
            else:
                time.sleep(1)
                is_preparing[iter] -= 1
        is_reset[iter] = False
                

def reset_media_player_snapshot_thread(iter):
    threading.Thread(target = reset_media_player_snapshot,args=[iter]).start()
        
    

#snapshot
def snapshot(iter,preset):
    if(media_player_snapshot[iter].is_playing() == 1 & is_preparing[iter] == 0):
        #media_player_snapshot[iter].next_frame()
        media_player_snapshot[iter].video_take_snapshot(0, get_preset_path(iter,preset),1920,1080)  
    else:
        count = 0
        while(is_preparing[iter] > 0 & count < 30):
            time.sleep(1)
            count+=1
            #print("count: " + str(count) + " prepare: " + str(is_preparing))
        if(count < 30):
            #media_player_snapshot[iter].next_frame()
            media_player_snapshot[iter].video_take_snapshot(0, get_preset_path(iter,preset),1920,1080)
        else:
            print("missing an Snapshot at camera " + str(iter) +" preset " + str(preset) + ": time out - network error")

#start record a preset
def start_record_preset(iter,preset):
    global media_player_records
    mediaName ="camera_" +str(iter) + "preset_" + str(preset) +"_" + datetime.now().strftime("%m-%d-%Y-%Hh%Mm%Ss") +".avi"
    media_record = vlcInstance[iter].media_new(camera_links[iter])
    media_record.add_option("sout=#std{access=file,mux=avi,dst="+get_video_preset_path(iter)+ "/" + mediaName+"}}")
    media_player_records[iter][preset].set_media(media_record)
    media_player_records[iter][preset].play()

#stop record a preset
def stop_record_preset(iter,preset):
    global media_player_records
    if(media_player_records[iter][preset]==1):
        media_player_records[iter][preset].stop()
        media_player_records[iter][preset].release()
    
def run_threaded(job_func,args):
    job_thread = threading.Thread(target=job_func,args=args)
    job_thread.start()   
# scheduling
camera = 0
while(camera < num_of_camera):
    preset = 0
    while(preset < num_of_preset):
        it = 0
        hour = int(preset/6) + 8
        
        while(it < 10):
            timeSnap=''
            if(hour<10):
                timeSnap+= '0'
            
            min = preset%6*10+it
            timeSnap += str(hour) + ":"
            
            if(min <10): 
                timeSnap = timeSnap + "0"+str(min) 
            else:
                timeSnap = timeSnap + str(min)
            timeSnapshot = timeSnap + ":30"
            timeResetSnapshot = timeSnap + ":00"
            # print(timeResetSnapshot)
            # schedule.every().day.at(timeResetSnapshot).do(reset_media_player_snapshot_thread,camera)
            # timeResetSnapshot = timeSnap + ":05"
            # schedule.every().day.at(timeResetSnapshot).do(reset_media_player_snapshot_thread,camera)
            # timeResetSnapshot = timeSnap + ":10"
            # schedule.every().day.at(timeResetSnapshot).do(reset_media_player_snapshot_thread,camera)
            # timeResetSnapshot = timeSnap + ":15"
            # schedule.every().day.at(timeResetSnapshot).do(reset_media_player_snapshot_thread,camera)
            # timeResetSnapshot = timeSnap + ":20"
            # schedule.every().day.at(timeResetSnapshot).do(reset_media_player_snapshot_thread,camera)
            # timeResetSnapshot = timeSnap + ":25"
            # schedule.every().day.at(timeResetSnapshot).do(reset_media_player_snapshot_thread,camera)
            # timeResetSnapshot = timeSnap + ":30"
            # schedule.every().day.at(timeResetSnapshot).do(reset_media_player_snapshot_thread,camera)
            # timeResetSnapshot = timeSnap + ":35"
            # schedule.every().day.at(timeResetSnapshot).do(reset_media_player_snapshot_thread,camera)
            # #print(timeResetSnapshot + " " + timeSnap)
            # # giây 10 kiểm tra nếu luồng bị ngắt hy vọng kết nối trước giây 30
            # schedule.every().day.at(timeResetSnapshot).do(reset_media_player_snapshot_thread,camera)
            # taking screen shot
            schedule.every().day.at(timeSnapshot).do(run_threaded,snapshot,[camera,preset])
            it += 1
            
        
        #find time start record
        hour_start_record =  hour
        min_start_record =preset%6*10
        
        if(min_start_record == 0):
            hour_start_record = hour_start_record - 1
            min_start_record = 59
        else:
            min_start_record -=1
        time_start_record = str(hour_start_record) + ":"    
        if(min_start_record <10): 
            time_start_record = time_start_record + "0"+str(min_start_record) 
        else:
            time_start_record = time_start_record + str(min_start_record)
            
        time_start_record = time_start_record + ":40"
        #print(time_start_record)
        # schedule.every().day.at(time_start_record).do(run_threaded,start_record_preset,[camera,preset])
        
        #find time stop record
        hour_stop_record =  hour
        min_stop_record = (preset+1)%6*10
        if(min_stop_record==0):
            hour_stop_record+=1
        time_stop_record = str(hour_stop_record) + ":"
        if(min_stop_record <10): 
            time_stop_record = time_stop_record + "0"+str(min_stop_record) 
        else:
            time_stop_record = time_stop_record + str(min_stop_record)   
        # schedule.every().day.at(time_stop_record).do(run_threaded,stop_record_preset,[camera,preset])
        #print(time_stop_record)
        
        preset += 1
    camera+=1
# Loop so that the scheduling task
# keeps on running all time.
d1 = datetime.now()
d1 = datetime(d1.year,d1.month,d1.day,10,1,0)
#print(get_video_preset_path())
while datetime.now() < d1:
 
    # Checks whether a scheduled task
    # is pending to run or not
    schedule.run_pending()
    time.sleep(1)
for i in range(num_of_camera):
    media_player_snapshot[i].stop()