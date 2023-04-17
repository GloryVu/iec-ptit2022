from datetime import datetime
import schedule
import vlc
import time
import os
import threading
#["--demux=ts ]
path = "D://iec_ptit_2022/cvanomaly_detection/record/record16h_18h/"

#get Preset Path
def get_path():
   
    if(os.path.exists(path) == False):
        os.makedirs(path)
    return path

vlcInstance = vlc.Instance("--demux=ts",b"--rtsp-frame-buffer-size=800000",b"--network-caching=1000")
media_player_records  = vlcInstance.media_player_new()
mediaName = datetime.now().strftime("%m-%d-%Y") +".avi"
media_record = vlcInstance.media_new("rtsp://iocldg:iocldg123123@10.1.20.18:554/profile1/media.smp")
media_record.add_option("sout=#std{access=file,mux=avi,dst="+get_path()+ "/" + mediaName+"}}")
media_player_records.set_media(media_record)
is_preparing = 0
is_reset = False
def reset_media_player_records():
    global is_reset
    global is_preparing
    if(media_player_records.is_playing() == 0 & is_reset == False):
        print("resetting stream")
        #global is_reset
        #global is_preparing
        is_reset = True
  
        #media_player_records.release();
        while(media_player_records.is_playing() == 0):
            media_player_records.stop()
            media_player_records.play()
            time.sleep(1)
 
        is_preparing = 20
        while(is_preparing > 0):
            
            if(media_player_records.is_playing() == 0):
                is_preparing = -1
            else:
                time.sleep(1)
                is_preparing -= 1
        is_reset = False
                
#start record a preset
def start_record():
    global media_player_records
    
    media_player_records.play()

#stop record a preset
def stop_record():
    global media_player_records
    media_player_records.stop()
    media_player_records.release()
    
    
# scheduling
time_start_record = "15:59:40"
schedule.every().day.at(time_start_record).do(start_record)
time_stop_record = "18:00:00"
schedule.every().day.at(time_stop_record).do(stop_record)
preset = 0
preset = 0
while(preset < 12):
    it = 0
    hour = int(preset/6) + 16
    
    while(it < 10):
        
        
        min = preset%6*10+it
        timeSnap = str(hour) + ":"
        
        if(min <10): 
            timeSnap = timeSnap + "0"+str(min) 
        else:
            timeSnap = timeSnap + str(min)
        timeReset = timeSnap + ":00"
        #print(timeReset)
        schedule.every().day.at(timeReset).do(reset_media_player_records)
        it+=1
    preset+=1
# Loop so that the scheduling task
# keeps on running all time.
d1 = datetime.now()
d1 = datetime(d1.year,d1.month,d1.day,18,1,0)

while datetime.now() < d1:
 
    # Checks whether a scheduled task
    # is pending to run or not
    schedule.run_pending()
    time.sleep(1)