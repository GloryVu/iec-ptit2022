from datetime import datetime
import schedule
import vlc
import time
import os
import threading
#["--demux=ts ]
record_path = r"D:\iec_ptit_2022\record\video_dataset"
snap_path =r"D:\iec_ptit_2022\record\images_dataset"
camera_links = ["rtsp://iocldg:iocldg123123@10.1.20.4:554/profile1/media.smp",
"rtsp://iocldg:iocldg123123@10.1.20.18:554/profile1/media.smp",
"rtsp://iocldg:iocldg123123@10.1.20.25:554/profile1/media.smp",
"rtsp://iocldg:iocldg123123@10.1.20.29:554/profile1/media.smp",
"rtsp://iocldg:iocldg123123@10.1.20.21:554/profile1/media.smp",]
num_of_camera = 5
num_of_preset=12
today = datetime.now().strftime("%m_%d_%Y")
presetName = 'preset'
#get Preset record_path
def get_record_path():
   
    if(os.path.exists(record_path) == False):
        os.makedirs(record_path)
    return record_path
vlcInstances = []
for i in range(num_of_camera):
    vlcInstances.append(vlc.Instance("--demux=ts",b"--rtsp-frame-buffer-size=800000",b"--network-caching=1000"))
media_player_records =[]
for i in range(num_of_camera):
    media_player_records.append(vlcInstances[i].media_player_new())
    
# make snapshot directory
def make_snap_dir(cam_idx,preset):
    dateFolder = today + '/'
    preset_path = snap_path + 'camera'+str(cam_idx)+'/'+ dateFolder + presetName+str(preset)
    if(os.path.exists(preset_path) == False):
        os.makedirs(preset_path)
    return preset_path
               
#start record a preset
def start_record():
    global media_player_records
    for i in range(num_of_camera):
        mediaName = 'camera_' + str(i) + '_' + str(datetime.now().strftime("%m_%d_%Y_%H_%M_%S")) +".avi"
        media_record = vlcInstances[i].media_new(camera_links[i])
        media_record.add_option("sout=#duplicate{dst=display,dst=standard{access=file,mux=avi,dst="+get_record_path() +'/' + mediaName+"}}")
        media_player_records[i].set_media(media_record)
    for i in range(num_of_camera):
        media_player_records[i].play()

#stop record a preset
def stop_record():
    global media_player_records
    for i in range(num_of_camera):
        media_player_records[i].stop()
        media_player_records[i].release()

def snapshot(cam_idx,preset):
    if(media_player_records[cam_idx].is_playing() == 1):
        media_player_records[cam_idx].video_take_snapshot(0, make_snap_dir(cam_idx,preset),1920,1080)  
    else:
        print("missing an Snapshot at camera " + str(cam_idx) +" preset " + str(preset) + ": time out - network error")

    
# scheduling
time_start_record = "08:57:00"
schedule.every().day.at(time_start_record).do(start_record)
time_stop_record = "11:57:00"
schedule.every().day.at(time_stop_record).do(stop_record)
time_start_record = "13:21:00"
schedule.every().day.at(time_start_record).do(start_record)
time_stop_record = "15:00:00"
schedule.every().day.at(time_stop_record).do(stop_record)
time_start_record = "15:36:00"
schedule.every().day.at(time_start_record).do(start_record)
time_stop_record = "17:00:00"
schedule.every().day.at(time_stop_record).do(stop_record)
# schedule.every().day.at('10:59').do(run_threaded,start_record,[])
# # stop record at 13:01
# schedule.every().day.at('13:01').do(run_threaded,stop_record,[])
# chạy 1 hàm như 1 luồng
def run_threaded(job_func,args):
    job_thread = threading.Thread(target=job_func,args=args)
    job_thread.start()   

camera = 0
while(camera < num_of_camera):
    # stop_record(camera)
    preset = 0
    while(preset < num_of_preset):
        it = 0
        hour = int(preset/6) + 13
        while(it < 10):
            min = preset%6*10+it
            timeSnap = str(hour) + ":"
            if(min <10): 
                timeSnap = timeSnap + "0"+str(min) 
            else:
                timeSnap = timeSnap + str(min)
            timeSnapshot = timeSnap + ":30"
            # taking screen shot
            schedule.every().day.at(timeSnapshot).do(run_threaded,snapshot,[camera,preset])
            it += 1
        preset += 1
    camera+=1
# preset = 0
# preset = 0
# while(preset < 12):
#     it = 0
#     hour = int(preset/6) + 16
    
#     while(it < 10):
        
        
#         min = preset%6*10+it
#         timeSnap = str(hour) + ":"
        
#         if(min <10): 
#             timeSnap = timeSnap + "0"+str(min) 
#         else:
#             timeSnap = timeSnap + str(min)
#         timeReset = timeSnap + ":00"
#         #print(timeReset)
#         schedule.every().day.at(timeReset).do(reset_media_player_records)
#         it+=1
#     preset+=1
# Loop so that the scheduling task
# keeps on running all time.
start_record()
d1 = datetime.now()
d1 = datetime(d1.year,d1.month,d1.day,17,1,0)

while datetime.now() < d1:
 
    # Checks whether a scheduled task
    # is pending to run or not
    schedule.run_pending()
    time.sleep(1)