"""
Server receiver of the file
"""
import socket
import os
import sys
import threading
IMGS_PATH = r'D:\iec_ptit_2022\process_data_app\detected_object\clips\\'
LABELS_PATH =r'D:\iec_ptit_2022\process_data_app\detected_object\labels\\'
# device's IP address
SERVER_HOST = "0.0.0.0"
SERVER_PORT = 5001
# receive 4096 bytes each time
BUFFER_SIZE = 1024*1024
SEPARATOR = "<SEPARATOR>"
# create the server socket
# TCP socket
import win32serviceutil
import win32service
import win32event
import servicemanager
import socket

def main():
        def recv_to_newline(s):
            buf = []
            while True:
                c = s.recv(1)
                if not len(c):
                    # socket closed
                    return None
                if c == b"\n":
                    return b"".join(buf)
                buf.append(c)

        def handle_client(client_socket, address):
            filename = recv_to_newline(client_socket).decode("utf-8")
            # print(filename)
            file_size = int(recv_to_newline(client_socket).decode("utf-8"))
            # print(file_size)
            filename = os.path.basename(filename)
            type = filename.split('.')[-1]
            file_path =''
            if type =='txt':
                file_path = LABELS_PATH+filename
            else:
                file_path = IMGS_PATH+filename
            with open(file_path, "wb") as f:
                while True:
                    # read 1024 bytes from the socket (receive)
                    bytes_read = client_socket.recv(BUFFER_SIZE)
                    if not bytes_read:    
                        # nothing is received
                        # file transmitting is done
                        break
                    # write to the file the bytes we just received
                    f.write(bytes_read)
                    # update the progress bar
                    # progress.update(len(bytes_read))

            # close the client socket
            client_socket.close()
            # close the server socket
            # s.close()
        s = socket.socket()
        # bind the socket to our local address
        s.bind((SERVER_HOST, SERVER_PORT))
        # enabling our server to accept connections
        # 5 here is the number of unaccepted connections that
        # the system will allow before refusing new connections
        s.listen(5)
        # print(f"[*] Listening as {SERVER_HOST}:{SERVER_PORT}")
        # accept connection if there is any
        while True:
            client_socket, address = s.accept() 
            # if below code is executed, that means the sender is connected
            # print(f"[+] {address} is connected.")
            thread = threading.Thread(target=handle_client, args=(client_socket, address))
            thread.start()
            # receive the file infos
            # receive using client socket, not server socket
if __name__ == '__main__':
    main()