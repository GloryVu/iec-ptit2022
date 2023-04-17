import time
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
import os
import shutil

def send(filename):
    #try:
        shutil.copyfile(IMGS_PATH+filename,TEMP_PATH+filename)
    #except:
    #    pass
    # host = HOST
    # port = PORT
    # send_file(filename, HOST, PORT)
IMGS_PATH = '/usr/share/hassio/media/frigate/clips/'
LABELS_PATH ='/usr/share/hassio/homeassistant/label/'
TEMP_PATH ='/home/lamdong/file_transfer_service/temp_file_transfer/'
def on_created(event):
    img_path = event.src_path
    img_name = os.path.basename(img_path)
    label_name = img_name.replace('.jpg','.txt')
    print(f"hey, {img_name} has been created!")
    send(img_name)
    # send(LABELS_PATH+label_name)

if __name__ == "__main__":
    patterns = ["*"]
    ignore_patterns = None
    ignore_directories = False
    case_sensitive = True
    my_event_handler = PatternMatchingEventHandler(patterns, ignore_patterns, ignore_directories, case_sensitive)
    my_event_handler.on_created = on_created
    path = IMGS_PATH
    go_recursively = True
    my_observer = Observer()
    my_observer.schedule(my_event_handler, path, recursive=go_recursively)

    my_observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        my_observer.stop()
        my_observer.join()
