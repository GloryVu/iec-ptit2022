import tkinter as tk
from tkinter.ttk import Button, Label, Entry
import tkinter.scrolledtext as ScrolledText
from tkinter import ttk
from PIL import ImageTk, Image  
# from tqdm.tk import tqdm
import os
import detected_object.classify_image as ci
import preprocess_data.tripmap as tm
import preprocess_data.split as sp
import detected_object.data_transfer as dt
import shutil
from retrain.train import train
import threading
import logging
import sys
import webbrowser
import re
from tqdm.gui import tqdm
import cv2 as cv
from ftp_deploy_model.ftp import file_transfer
import sys

# import tkinterweb
# link = Label(win, text="www.tutorialspoint.com",font=('Helveticabold', 15), fg="blue", cursor="hand2")

# class TextHandler(logging.Handler):
#     # This class allows you to log to a Tkinter Text or ScrolledText widget
#     # Adapted from Moshe Kaplan: https://gist.github.com/moshekaplan/c425f861de7bbf28ef06

#     def __init__(self, text):
#         # run the regular Handler __init__
#         logging.Handler.__init__(self)
#         # Store a reference to the Text it will log to
#         self.text = text

#     def emit(self, record):
#         msg = self.format(record)
#         def append():
#             self.text.configure(state='normal')
#             self.text.insert(tk.END, msg + '\n')
#             self.text.configure(state='disabled')
#             # Autoscroll to the bottom
#             self.text.yview(tk.END)
#         # This is necessary because we can't modify the Text from other threads
#         self.text.after(0, append)
class IORedirector(object):
    '''A general class for redirecting I/O to this Text widget.'''
    def __init__(self,text_area):
        self.text_area = text_area

class StdoutRedirector(object):
    '''A class for redirecting stdout to this Text widget.'''
    def __init__(self,text_area):
        self.text_area = text_area
    def write(self,str):
        # self.text_area.write(str,False)
        self.text_area.insert(tk.END, str + '\n')
    def flush(self):
        # self.text_area.write('',True)
        pass
# To start redirecting stdout:

# sys.stdout = StdoutRedirector()
# (where self refers to the widget)

# To stop redirecting stdout:
# sys.stdout = sys.__stdout__
def check_sample(img):
    # print(os.stat('detected_object/clips/' + img))
    name = img.replace('.jpg','')    
    if not os.path.exists('detected_object/clips/' + name + '-clean.png'):
        print('not exists -clean' + 'detected_object/clips/' + name + '-clean.png')
        return True
    if not os.path.exists('detected_object/labels/' + name + '.txt'):
        print('not exists label')
        return True
    if os.stat('detected_object/labels/' + name + '.txt').st_size < 500:
        print('label missing')
        return True
    if os.stat('detected_object/clips/' + name + '-clean.png').st_size < 1024:
        print('-clean missing')
        return True    
    if os.stat('detected_object/clips/' + img).st_size < 1024:
        print('bbox img missing')
        return True 
    # try:
    try:
        img_mat = cv.imread('detected_object/clips/' + name + '-clean.png')    
        img_mat.shape
    except:
        print('-clean image not completed transfer')
        return True 
    try:
        img_mat = cv.imread('detected_object/clips/' + img)
        img_mat.shape
    # img.shape[0]
    # img.shape[1]
    except:
        print('bbox image not completed transfer')
        return True 
    # return False

def init():
    # print(check_sample('camera_10_1_20_16-1680088183.559586-5rtotx.jpg'))
    global img_list,verified_img_dict,unverified_img_list,current_idx, unverified_idx_list,current_unverified_idx
    img_list = os.listdir('detected_object/clips')
    # print(os.curdir)
    # print(img_list)
    # pattern = "(.+).jpg"
    # print(img_list)
    # print(len(img_list))
    
    for img in img_list:
        # print(re.match(pattern,img))
        # print(img)
        # print((img.split('.')[-1]))
        if(img.split('.')[-1]!='jpg'):  
            # print(img)
            # print('remove ' + img)
            img_list.remove(img)
        # if check_sample(img):
            # print(check_sample(img))
            # img_list.remove(img)
    f = open('detected_object/prechecked_img_list.txt')
    data = f.read()
    lines  = data.splitlines()
    lines  = [line.split(' ') for line in lines]
    checked_img ={}
    for img,verify in lines:
        checked_img[img]= int(verify)
    f.close()
    img_list = [img for img in img_list if (img not in checked_img.keys()) or checked_img[img]==1]
    unchecked_img = [img for img in img_list if img not in checked_img.keys()]
    tqdm_bar = tqdm(unchecked_img,'khởi tạo dữ liệu',)
    for img in tqdm_bar:
        if img not in checked_img.keys():
            if check_sample(img):
                img_list.remove(img)
                checked_img[img] = 0
            else:
                checked_img[img] = 1
        else:
            if checked_img[img] == 0:
                img_list.remove(img)
    # tqdm_bar.
    with open('detected_object/prechecked_img_list.txt','w') as f:
        f.writelines(img+' ' +str(checked_img[img])+'\n' for img in checked_img.keys())  

    # print(len(img_list))        
    f = open('detected_object/verified_img_list.txt')
    data = f.read()
    lines  = data.splitlines()
    lines  = [line.split(' ') for line in lines]
    verified_img_dict ={}
    for img,verify in lines:
        verified_img_dict[img]= int(verify)
    unverified_idx_list =[i for i in range(len(img_list)) if img_list[i] not in verified_img_dict.keys()]
    current_idx = -1
    current_unverified_idx = -1
    next()
def read_image(file):
    img = Image.open(file)
    img = img.resize((50, 50), Image.ANTIALIAS)
    return img

def set_image(label,img):
    # img = cv.imread(img)
    test = ImageTk.PhotoImage(Image.open(img).resize([400,400]))

    label = tk.Label(frm_label_img,image=test)
    label.image = test
    label.grid(row=0, column=1, sticky="nsew")

def set_label_saved(var):
    if(var!=-1):
        text = 'Đã lưu: '
        if var == 1:
            text +='Đúng'
        else: text += 'Sai'
    else:
        text = 'Chưa xác nhận'
    var_label_saved.set(text)
    
def next():
    global current_idx
    if(current_idx<len(img_list)-1):
        current_idx +=1
        set_image(frm_label_img,'detected_object/clips/'+img_list[current_idx])
        if img_list[current_idx] in verified_img_dict.keys():
            var = verified_img_dict[img_list[current_idx]]
            var_v.set(var)
            set_label_saved(var)
        else:
            set_label_saved(-1)
        root.update_idletasks()
        
def previous():
    global current_idx
    if(current_idx>0):
        current_idx -=1
        set_image(frm_label_img,'detected_object/clips/'+img_list[current_idx])
        if img_list[current_idx] in verified_img_dict.keys():
            var = verified_img_dict[img_list[current_idx]]
            var_v.set(var)
            set_label_saved(var)
        else:
            set_label_saved(-1)
        root.update_idletasks()
                
def next_unverified():
    global current_idx, current_unverified_idx
    if(current_unverified_idx<len(unverified_idx_list)-1):
        current_unverified_idx+=1
        current_idx = unverified_idx_list[current_unverified_idx]
        set_image(frm_label_img,'detected_object/clips/'+img_list[current_idx])
        if img_list[current_idx] in verified_img_dict.keys():
            var = verified_img_dict[img_list[current_idx]]
            var_v.set(var)
            set_label_saved(var)
        else:
            set_label_saved(-1)
        root.update_idletasks()
               
def previous_unverified():
    global current_idx, current_unverified_idx
    if(current_unverified_idx>0):
        current_unverified_idx-=1
        current_idx = unverified_idx_list[current_unverified_idx]
        set_image(frm_label_img,'detected_object/clips/'+img_list[current_idx])
        if img_list[current_idx] in verified_img_dict.keys():
            var = verified_img_dict[img_list[current_idx]]
            var_v.set(var)
            set_label_saved(var)
        else:
            set_label_saved(-1)
        root.update_idletasks()        

def save_current():
    verified_img_dict[img_list[current_idx]] = var_v.get()
    try: 
        unverified_idx_list.remove(current_idx)
    except:
        pass
def save_all():
    f = open('detected_object/verified_img_list.txt','w')
    f.writelines(img+' ' +str(verified_img_dict[img])+'\n' for img in verified_img_dict.keys())  

def preprocess_data():
    # đọc dữ liệu đã lưu
    imgs = ci.process_data()
    # i = 0
    # var_label_bpar.set('đọc dữ liệu đã lưu:')
    # var_label_progress.set('tiến độ: 0/'+str(len(imgs)))
    # root.update_idletasks()
    for img,ver in tqdm(imgs,'đọc file nhãn'):
        ci.process_each_data(img,ver)
        # i+=1
        # bpar['value'] = int(1.0*i/len(imgs)*100)
        
        # var_label_progress.set('tiến độ: '+str(i)+'/'+str(len(imgs)))
        # root.update_idletasks()
    
    # tạo ảnh trimaps
    # i = 0
    # var_label_bpar.set('tiền xử lý:')
    # var_label_progress.set('tiến độ: 0/'+str(len(imgs)))
    # root.update_idletasks()
    imgs =tm.get_list_file()
    for img in tqdm(imgs,'tiền xử lý'):
        tm.process_each_trimap(img)
        # i+=1
        # bpar['value'] = int(1.0*i/len(imgs)*100)
        # var_label_progress.set('tiến độ: '+str(i)+'/'+str(len(imgs)))
        # root.update_idletasks()
    
    #write list file
    var_label_bpar.set('write list file:')
    var_label_progress.set('tiến độ: 0/1')
    bpar['value'] = 0
    root.update_idletasks()
    sp.write_list_to_file()
    bpar['value'] = 100
    var_label_progress.set('tiến độ: 1/1')
    root.update_idletasks()
    
def transfer_data():
    # chuyển file
    list = dt.get_list_copy_path()   
    # i = 0
    # var_label_bpar.set('chuyển dữ liệu:')
    # var_label_progress.set('tiến độ: 0/'+str(len(list)))
    # root.update_idletasks()
    for src,dist in tqdm(list,'chuyển dữ liệu'):
        shutil.copyfile(src,dist)
        # i+=1
        # bpar['value'] = int(1.0*i/len(list)*100)
        # var_label_progress.set('tiến độ: '+str(i)+'/'+str(len(list)))
        # root.update_idletasks()
    
    # cập nhật list
    var_label_bpar.set('write list file:')
    var_label_progress.set('tiến độ: 0/1')
    bpar['value'] = 0
    root.update_idletasks()
    dt.write_list_file()
    bpar['value'] = 100
    var_label_progress.set('tiến độ: 1/1')
    root.update_idletasks()

def launch_tfboard():
    if var_v_retrain.get() == 0:
        os.system('tensorboard --logdir=retrain/smoke/train')
    if var_v_retrain.get() == 1:
        os.system('tensorboard --logdir=retrain/vacantland/train')
    if var_v_retrain.get() == 2:
        os.system('tensorboard --logdir=retrain/foundationhouse/train')
    if var_v_retrain.get() == 3:
        os.system('tensorboard --logdir=retrain/all/train')
#     tfboard.load_website('http://vms-02:6006/')
# def reload_tfboard():
#     tfboard.load_website('https://google.com')
def retrain():
    threading.Thread(target=train,args=[var_v_retrain.get()]).start()
    threading.Thread(target=launch_tfboard).start()
    # reload_tfboard()
def callback():
   webbrowser.open_new_tab('http://vms-02:6006/')
def deploy_model():
    if var_v_retrain.get() == 0:
        file_transfer('retrain/smoke/output_ssdlite_mobiledet/smoke.tflite')
    if var_v_retrain.get() == 1:
        file_transfer('retrain/vacantland/output_ssdlite_mobiledet/vacantland.tflite')
    if var_v_retrain.get() == 2:
        file_transfer('retrain/foundationhouse/output_ssdlite_mobiledet/foundationhouse.tflite')
    if var_v_retrain.get() == 3:
        file_transfer('retrain/all/output_ssdlite_mobiledet/all.tflite')
def main():
    
    global root,frm_label_img, frm_select, var_v, var_label_saved,R1,R2
    root = tk.Tk()
    # root.geometry('1080x650')
    root.title('Process Data')
    notebook = ttk.Notebook(root)
    notebook.pack(pady=10, expand=True)
    frame_verify = tk.Frame(notebook,width=1000,height=600)
    frame_processdata = tk.Frame(notebook,width=1000,height=600)
    frame_retrain = tk.Frame(notebook,width=1000,height=600)
    
    #frame_verify
    frame_verify.columnconfigure(1, minsize=600, weight=1)
    frm_label_img = tk.Label(frame_verify)
    frm_buttons = tk.Frame(frame_verify, relief=tk.RAISED, bd=2)
    frm_select = tk.Frame(frame_verify, relief=tk.RAISED, bd=2)
    btn_open = tk.Button(frm_buttons, text="Save All", command=save_all)
    btn_save = tk.Button(frm_buttons, text="Save", command=save_current,)
    btn_next = tk.Button(frm_buttons, text="Next", command=next,)
    btn_previous = tk.Button(frm_buttons, text="Previos", command=previous,)
    btn_next_unverify = tk.Button(frm_buttons, text="Next Unverified", command=next_unverified,)
    btn_previous_unverify = tk.Button(frm_buttons, text="Previos Unverified", command=previous_unverified,)
    btn_refresh = tk.Button(frm_buttons, text="Refresh", command=init,)
    label_question = tk.Label(frm_select,text='kết quả nhận diện?')
    var_v = tk.IntVar(frm_select)
    var_label_saved = tk.StringVar()
    label_saved = tk.Label(frm_select,textvariable=var_label_saved)
    R1 = tk.Radiobutton(frm_select, text="Đúng", variable=var_v, value=1, indicatoron=False)
    R2 = tk.Radiobutton(frm_select, text="Sai", variable=var_v, value=0, indicatoron=False)
    R1.grid(row=1, column=3, sticky="ew", padx=5, pady=5)
    R2.grid(row=2, column=3, sticky="ew", padx=5, pady=5)
    btn_open.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
    btn_save.grid(row=1, column=0, sticky="ew", padx=5)
    btn_next.grid(row=2, column=0, sticky="ew", padx=5, pady=5)
    btn_previous.grid(row=3, column=0, sticky="ew", padx=5, pady=5)
    btn_next_unverify.grid(row=4, column=0, sticky="ew", padx=5, pady=5)
    btn_previous_unverify.grid(row=5, column=0, sticky="ew", padx=5, pady=5)
    btn_refresh.grid(row=6, column=0, sticky="ew", padx=5, pady=5)
    frm_buttons.grid(row=0, column=0, sticky="ns")
    frm_label_img.grid(row=0, column=1, sticky="nsew")
    frm_select.grid(row=0, column=2, sticky="en")
    label_question.grid(row=0, column=3, sticky="ew", padx=5, pady=5)
    label_saved.grid(row=3, column=3, sticky="ew", padx=5, pady=5)
    init()
    
    if(current_idx!=-1):
        set_image(frm_label_img,'detected_object/clips/'+img_list[current_idx])

    # frame_processdata
    
    global bpar, frm_progress, var_label_progress, var_label_bpar
    frm_progress = tk.Frame(frame_processdata, relief=tk.RAISED, bd=2)
    frm_buttons1 = tk.Frame(frame_processdata, relief=tk.RAISED, bd=2)
    bpar = ttk.Progressbar(frm_progress,length=500, mode='determinate')
    var_label_bpar = tk.StringVar()
    var_label_progress = tk.StringVar()
    label_bpar = tk.Label(frm_progress,textvariable = var_label_bpar)
    label_progress = tk.Label(frm_progress, textvariable = var_label_progress)
    btn_preprocessdata = tk.Button(frm_buttons1, text="Preprocess Data", command=preprocess_data)
    btn_data_transfer = tk.Button(frm_buttons1, text="Transfer Data", command=transfer_data,)
    # btn_next1 = tk.Button(frm_buttons1, text="Next", command=next,)
    # btn_previous1 = tk.Button(frm_buttons1, text="Previos", command=previous,)
    # btn_next_unverify1 = tk.Button(frm_buttons1, text="Next Unverified", command=next_unverified,)
    # btn_previous_unverify1 = tk.Button(frm_buttons1, text="Previos Unverified", command=previous_unverified,)
    btn_preprocessdata.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
    btn_data_transfer.grid(row=1, column=0, sticky="ew", padx=5, pady=5)
    # btn_next1.grid(row=2, column=0, sticky="ew", padx=5, pady=5)
    # btn_previous1.grid(row=3, column=0, sticky="ew", padx=5, pady=5)
    # btn_next_unverify1.grid(row=4, column=0, sticky="ew", padx=5, pady=5)
    # btn_previous_unverify1.grid(row=5, column=0, sticky="ew", padx=5, pady=5)
    frm_buttons1.grid(row=0, column=0, sticky="ns")
    frm_progress.grid(row=0, column=1, sticky="nsew")
    
    label_bpar.grid(row=0, column=1, sticky="ew")
    bpar.grid(row=1, column=1, sticky="nsew")
    label_progress.grid(row=2, column=1, sticky="nsew")

    # frame_retrain
    global  var_v_retrain, frm_progress_retrain, var_label_progress_retrain, var_label_bpar_retrain
    frm_progress_retrain = tk.Frame(frame_retrain, relief=tk.RAISED, bd=2)
    frm_buttons1_retrain = tk.Frame(frame_retrain, relief=tk.RAISED, bd=2)
    frm_select_retrain = tk.Frame(frame_retrain, relief=tk.RAISED, bd=2)
    # bpar_retrain = ttk.Progressbar(frm_progress_retrain,length=500, mode='determinate')
    var_label_bpar_retrain = tk.StringVar()
    var_label_progress_retrain = tk.StringVar()
    # label_bpar_retrain = tk.Label(frm_progress_retrain,textvariable = var_label_bpar_retrain)
    # label_progress_retrain = tk.Label(frm_progress_retrain, textvariable = var_label_progress_retrain)
    btn_retrain = tk.Button(frm_buttons1_retrain, text="Retrain", command=retrain)
    btn_deploy_model = tk.Button(frm_buttons1_retrain, text="Deploy Model", command=deploy_model,)
    btn_reload_tfboard = tk.Button(frm_buttons1_retrain, text="Tensor Board", command=callback)
    text_logger =   tk.Text(frm_progress_retrain,)
    btn_retrain.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
    btn_deploy_model.grid(row=1, column=0, sticky="ew", padx=5, pady=5)
    btn_reload_tfboard.grid(row=2, column=0, sticky="ew", padx=5, pady=5)
    #Define a callback function


#Create a Label to display the link
    # link = Label(frm_progress_retrain, text="'http://vms-02:6006/",font=('Helveticabold', 15), fg="blue", cursor="hand2")
    # link.pack()
    # link.bind("<Button-1>", lambda e:
    # callback("http://vms-02:6006/"))

    # btn_next1.grid(row=2, column=0, sticky="ew", padx=5, pady=5)
    # btn_previous1.grid(row=3, column=0, sticky="ew", padx=5, pady=5)
    # btn_next_unverify1.grid(row=4, column=0, sticky="ew", padx=5, pady=5)
    # btn_previous_unverify1.grid(row=5, column=0, sticky="ew", padx=5, pady=5)
    frm_buttons1_retrain.grid(row=0, column=0, sticky="ns")
    frm_progress_retrain.grid(row=0, column=1, sticky="nsew")
    frm_select_retrain.grid(row=0, column=2, sticky="en")
    text_logger.grid(row=0, column=1, sticky="ew")
    label_question_retrain = tk.Label(frm_select_retrain,text='Chọn loại mô hình:')
    var_v_retrain = tk.IntVar(frm_select)
    # var_label_saved = tk.StringVar()
    # label_saved = tk.Label(frm_select,textvariable=var_label_saved)
    
    R1_retrain = tk.Radiobutton(frm_select_retrain, text="Khói cháy", variable=var_v_retrain, value=0, indicatoron=False)
    R2_retrain = tk.Radiobutton(frm_select_retrain, text="Đất trống", variable=var_v_retrain, value=1, indicatoron=False)
    R3_retrain = tk.Radiobutton(frm_select_retrain, text="Móng nhà", variable=var_v_retrain, value=2, indicatoron=False)
    R4_retrain = tk.Radiobutton(frm_select_retrain, text="All", variable=var_v_retrain, value=3, indicatoron=False)
    label_question_retrain.grid(row=0, column=3, sticky="ew", padx=5, pady=5)
    R1_retrain.grid(row=1, column=3, sticky="ew", padx=5, pady=5)
    R2_retrain.grid(row=2, column=3, sticky="ew", padx=5, pady=5)
    R3_retrain.grid(row=3, column=3, sticky="ew", padx=5, pady=5)
    R4_retrain.grid(row=4, column=3, sticky="ew", padx=5, pady=5)
    # tfboard.grid(row=0, column=1, sticky="ew")
    # label_bpar_retrain.grid(row=0, column=1, sticky="ew")
    # bpar_retrain.grid(row=1, column=1, sticky="nsew")
    # label_progress_retrain.grid(row=2, column=1, sticky="nsew")
    # Add text widget to display logging info
    sys.stdout = StdoutRedirector(text_area=text_logger)
        # configure the nameless "root" logger to also write           # added
        # to the redirected sys.stdout                                 # added
    logger = logging.getLogger()                                   # added
    console = logging.StreamHandler(stream=sys.stdout)             # added
    logger.addHandler(console)
    notebook.add(frame_verify,text = 'verify data')
    notebook.add(frame_processdata,text = 'process data')
    notebook.add(frame_retrain,text = 'retrain')
    root.mainloop()
        
if __name__ == '__main__':
    # os.chdir('D:\iec_ptit_2022\process_data_app')
    # os.environ['PYTHONPATH'] += ':D:\iec_ptit_2022\process_data_app\retrain\models\models\research''
    # os.environ['PYTHONPATH'] += ':/content/models/research/slim/'
    # os.environ['PYTHONPATH'] += ':/content/models/research/object_detection/utils/'
    # os.environ['PYTHONPATH'] += ':/content/models/research/object_detection'
    # sys.path.append(r'D:\iec_ptit_2022\process_data_app\retrain\models\research')
    # sys.path.append(r'D:\iec_ptit_2022\process_data_app\retrain\models\research\slim')
    # sys.path.append(r'D:\iec_ptit_2022\process_data_app\retrain\models\research\object_detection\utils')
    # sys.path.append(r'D:\iec_ptit_2022\process_data_app\retrain\models\research\object_detection')
    main()
