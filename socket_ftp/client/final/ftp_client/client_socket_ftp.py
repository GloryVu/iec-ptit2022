import time
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
import os
import socket
# import shutil
"""
Client that sends the file (uploads)
"""

SEPARATOR = "<SEPARATOR>"
BUFFER_SIZE = 1024*1024 #4KB
HOST = '10.16.67.12'
PORT = 5001
def send_file(filename, host, port):
    # get the file size
    filesize = os.path.getsize(filename)
    # create the client socket
    s = socket.socket()
    print(f"[+] Connecting to {host}:{port}")
    s.connect((host, port))
    print("[+] Connected.")

    # send the filename and filesize
    s.sendall(filename.encode("utf-8"))
    s.sendall(b"\n")
    s.sendall(str(filesize).encode("utf-8"))
    s.sendall(b"\n")
    # start sending the file
    # progress = tqdm.tqdm(range(filesize), f"Sending {filename}", unit="B", unit_scale=True, unit_divisor=1024)
    with open(filename, "rb") as f:
        while True:
            # read the bytes from the file
            bytes_read = f.read(BUFFER_SIZE)
            if not bytes_read:
                # file transmitting is done
                break
            # we use sendall to assure transimission in 
            # busy networks
            s.sendall(bytes_read)
            # update the progress bar
            # progress.update(len(bytes_read))

    # close the socket
    s.close()

def send(filename):
    # host = HOST
    # port = PORT
    send_file(filename, HOST, PORT)
    os.remove(filename)
    # host = HOST
    # port = PORT
    # send_file(filename, HOST, PORT)
IMGS_PATH = '/usr/share/hassio/media/frigate/clips/'
LABELS_PATH ='/usr/share/hassio/homeassistant/label/'
TEMP_PATH ='/home/lamdong/file_transfer_service/temp_file_transfer/'
def on_created(event):
    img_path = event.src_path
    img_name = os.path.basename(img_path)
    # label_name = img_name.replace('.jpg','.txt')
    print(f"hey, {img_name} has been created!")
    send(TEMP_PATH + img_name)
    # send(LABELS_PATH+label_name)

if __name__ == "__main__":
    patterns = ["*"]
    ignore_patterns = None
    ignore_directories = False
    case_sensitive = True
    my_event_handler = PatternMatchingEventHandler(patterns, ignore_patterns, ignore_directories, case_sensitive)
    my_event_handler.on_created = on_created
    path = TEMP_PATH
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
