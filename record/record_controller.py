from datetime import datetime
import schedule
import vlc
import time
import os
import threading
#["--demux=ts ]
def init():
    global list_urls, num_of_cams, num_of_presets, path, preset, media_players
    list_urls = ["rtsp://iocldg:iocldg123123@10.1.20.4:554/profile1/media.smp",
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
    "rtsp://iocldg:iocldg123123@10.1.20.28:554/profile1/media.smp",
    "rtsp://iocldg:iocldg123123@10.1.10.207:554/cam/realmonitor?channel=1&subtype=0"]

    num_of_cams = len(list_urls)
    num_of_presets = 12

    path = "D://iec_ptit_2022/record/image_data_set/"

    vlc_instances = [vlc.Instance() for i in range(num_of_cams)]
    media_players = [vlc_instances[i].media_player_new() for i in range(num_of_cams)]
        
    medias = [vlc_instances[i].media_new(list_urls[i]) for i in range(num_of_cams)]

    #medias.get_mrl()
    # setting media to the media player
    for i in range(num_of_cams):
        media_players[i].set_media(medias[i])
    
    # setting video scale
    for i in range(num_of_cams):
        media_players[i].video_set_scale(0.3)  
    # start playing video
    for i in range(num_of_cams):
        media_players[i].play()

    
#get Preset Path
def make_prest_path(cam_idx,preset):
    dateFolder = datetime.now().strftime("%m-%d-%Y") + '/'
    presetPath = path + 'camera'+str(cam_idx)+'/'+ dateFolder + "preset"+str(preset)
    if(os.path.exists(presetPath) == False):
        os.makedirs(presetPath)
    return presetPath

#snapshot
def snapshot(cam_idx,preset):
    if(media_players[cam_idx].is_playing() == 1):
        media_players[cam_idx].video_take_snapshot(0, make_prest_path(cam_idx,preset),1920,1080)  
    else:
        print("missing an Snapshot at camera " + str(cam_idx) +" preset " + str(preset) + ": time out - network error")

def run_threaded(job_func,args):
    job_thread = threading.Thread(target=job_func,args=args)
    job_thread.start()   
# scheduling
def make_schedule():

    camera = 0
    while(camera < num_of_cams):
        preset = 0
        while(preset < num_of_presets):
            it = 0
            hour = int(preset/6) + 14
            
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
# Loop so that the scheduling task
# keeps on running all time.
def main():
    init()
    make_schedule()
    d1 = datetime.now()
    d1 = datetime(d1.year,d1.month,d1.day,16,1,0)
    #print(get_video_preset_path())
    while datetime.now() < d1:
        # Checks whether a scheduled task
        # is pending to run or not
        schedule.run_pending()
        time.sleep(1)
if __name__ == '__main__':
    main()