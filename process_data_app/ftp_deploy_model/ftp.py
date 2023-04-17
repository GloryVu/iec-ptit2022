from ftplib import FTP
import os
ftp_ip = "192.168.130.136"
ftp_usr = "lamdong@ptit"
ftp_pwd = "Lamdong@ptit"
dst_path = '../../usr/share/hassio/homeassistant'
def file_transfer(source_path):
    file_name = os.path.basename(source_path)
    ftp_client = FTP(ftp_ip)
    print(ftp_client.login(user=ftp_usr, passwd = ftp_pwd))
    print(ftp_client.pwd())
    ftp_client.cwd(dst_path)
    # print(ftp_client.cwd(".."))
    # print(ftp_client.cwd(".."))
    print(ftp_client.pwd())
    file_stream = open(source_path,"rb") 

    # send the file       
    ftp_client.storbinary("{CMD} {FileName}".
                format(CMD="STOR",FileName=file_name),
                file_stream)     
    file_stream.close() 
    print('file transfer successful: ' + file_name)
if __name__ =='__main__':
    file_transfer('ftp.py')