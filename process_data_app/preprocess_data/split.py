import random
import os
src_imgs = 'detected_object/output_data/images/'
src_xmls = 'detected_object/output_data/annotations/xmls/'
src_list = 'detected_object/output_data/list/'
from pascal import PascalVOC
def get_label_from_file(file):
    ann = PascalVOC.from_xml(file)
    for obj in ann.objects:
        return obj.name 

def write_list_to_file():
    list_file = os.listdir(src_imgs)
    random.shuffle(list_file)
    list_label = [get_label_from_file(src_xmls+file.split('.jpg')[0]+'.xml') for file in list_file]
    listfile = open(src_list+'list.txt','w')
    trainfile = open(src_list+"train.txt", "w")
    valfile = open(src_list+"val.txt",'w')
    p = int(len(list_file)*0.8)
    list_name = [name.split('.jpg')[0]+' 1 1 1' for name in list_file]
    for name in list_name:
        listfile.writelines(name +'\n')
    for name in list_name[:p]:
        trainfile.writelines(name +'\n')
    for name in list_name[p:]:
        valfile.writelines(name +'\n')
    listfile.close()
    trainfile.close()
    valfile.close()
    list_smoke = []
    for i in range(len(list_file)):
        if(list_label[i]=='smoke' or list_label[i]=='notsmoke'):
            list_smoke.append(list_file[i])
    listfile = open(src_list+'listsmoke.txt','w')
    trainfile = open(src_list+"trainsmoke.txt", "w")
    valfile = open(src_list+"valsmoke.txt",'w')
    p = int(len(list_smoke)*0.8)
    list_name = [name.split('.jpg')[0]+' 1 1 1' for name in list_smoke]
    for name in list_name:
        listfile.writelines(name +'\n')
    for name in list_name[:p]:
        trainfile.writelines(name +'\n')
    for name in list_name[p:]:
        valfile.writelines(name +'\n')
    listfile.close()
    trainfile.close()
    valfile.close()
    list_vacantland =[]
    for i in range(len(list_file)):
        if(list_label[i]=='vacantland' or list_label[i]=='notvacantland'):
            list_vacantland.append(list_file[i])
    listfile = open(src_list+'listvacantland.txt','w')
    trainfile = open(src_list+"trainvacantland.txt", "w")
    valfile = open(src_list+"valvacantland.txt",'w')
    p = int(len(list_vacantland)*0.8)
    list_name = [name.split('.jpg')[0]+' 1 1 1' for name in list_vacantland]
    for name in list_name:
        listfile.writelines(name +'\n')
    for name in list_name[:p]:
        trainfile.writelines(name +'\n')
    for name in list_name[p:]:
        valfile.writelines(name +'\n')
    listfile.close()
    trainfile.close()
    valfile.close()
    list_foundationhouse =[]
    for i in range(len(list_file)):
        if(list_label[i]=='foundationhouse' or list_label[i]=='notfoundationhouse'):
            list_foundationhouse.append(list_file[i])
    listfile = open(src_list+'listfoundationhouse.txt','w')
    trainfile = open(src_list+"trainfoundationhouse.txt", "w")
    valfile = open(src_list+"valfoundationhouse.txt",'w')
    p = round(len(list_foundationhouse)*0.8)
    list_name = [name.split('.jpg')[0]+' 1 1 1' for name in list_foundationhouse]
    for name in list_name:
        listfile.writelines(name +'\n')
    for name in list_name[:p]:
        trainfile.writelines(name +'\n')
    for name in list_name[p:]:
        valfile.writelines(name +'\n')
    listfile.close()
    trainfile.close()
    valfile.close()