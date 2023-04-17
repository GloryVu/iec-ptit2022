def read_list(path):
    f = open(path,'r')
    data = f.read()
    data  = data.splitlines()
    data  = [sample.split(' ')[0] for sample in data]
    return data
    
def get_list_copy_path():
    src = 'detected_object/output_data/'
    dist = 'retrain/'
    src_dist_list =[]
    list = read_list(src+'list/list.txt')
    imgs =['images/'+sample+'.jpg' for sample in list]
    trimaps =['annotations/trimaps/'+sample+'.png' for sample in list]
    xmls = ['annotations/xmls/'+sample+'.xml' for sample in list]
    for img in imgs:
        src_dist_list.append([src+img,dist+'all/dataset/'+img])
    for trimap in trimaps:
        src_dist_list.append([src+trimap,dist+'all/dataset/'+trimap])
    for xml in xmls:
        src_dist_list.append([src+xml,dist+'all/dataset/'+xml])   
    list = read_list(src+'list/listfoundationhouse.txt')
    imgs =['images/'+sample+'.jpg' for sample in list]
    trimaps =['annotations/trimaps/'+sample+'.png' for sample in list]
    xmls = ['annotations/xmls/'+sample+'.xml' for sample in list]
    for img in imgs:
        src_dist_list.append([src+img,dist+'foundationhouse/dataset/'+img])
    for trimap in trimaps:
        src_dist_list.append([src+trimap,dist+'foundationhouse/dataset/'+trimap])
    for xml in xmls:
        src_dist_list.append([src+xml,dist+'foundationhouse/dataset/'+xml])      
    list = read_list(src+'list/listsmoke.txt')
    imgs =['images/'+sample+'.jpg' for sample in list]
    trimaps =['annotations/trimaps/'+sample+'.png' for sample in list]
    xmls = ['annotations/xmls/'+sample+'.xml' for sample in list]
    for img in imgs:
        src_dist_list.append([src+img,dist+'smoke/dataset/'+img])
    for trimap in trimaps:
        src_dist_list.append([src+trimap,dist+'smoke/dataset/'+trimap])
    for xml in xmls:
        src_dist_list.append([src+xml,dist+'smoke/dataset/'+xml])  
    list = read_list(src+'list/listvacantland.txt')
    imgs =['images/'+sample+'.jpg' for sample in list]
    trimaps =['annotations/trimaps/'+sample+'.png' for sample in list]
    xmls = ['annotations/xmls/'+sample+'.xml' for sample in list]
    for img in imgs:
        src_dist_list.append([src+img,dist+'vacantland/dataset/'+img])
    for trimap in trimaps:
        src_dist_list.append([src+trimap,dist+'vacantland/dataset/'+trimap])
    for xml in xmls:
        src_dist_list.append([src+xml,dist+'vacantland/dataset/'+xml])    
    return src_dist_list

def _write_each_file(src,dst):
    dst_dict ={}
    fin = open(src,'r')
    din = fin.read()
    din = din.splitlines()
    fout = open(dst,'r')
    dout = fout.read()
    dout = dout.splitlines()
    for line in dout:
        dst_dict[line] =1
    fout = open(dst,'a')    
    for line in din:
        if line not in dst_dict.keys():
            fout.writelines(line+'\n')
    fout.close()
        
def write_list_file():
    src_dist_list = [['detected_object/output_data/list/list.txt','retrain/all/dataset/annotations/list.txt'],
                     ['detected_object/output_data/list/train.txt','retrain/all/dataset/annotations/train.txt'],
                     ['detected_object/output_data/list/val.txt','retrain/all/dataset/annotations/val.txt'],
                     ['detected_object/output_data/list/listfoundationhouse.txt','retrain/foundationhouse/dataset/annotations/list.txt'],
                     ['detected_object/output_data/list/trainfoundationhouse.txt','retrain/foundationhouse/dataset/annotations/train.txt'],
                     ['detected_object/output_data/list/valfoundationhouse.txt','retrain/foundationhouse/dataset/annotations/val.txt'],
                     ['detected_object/output_data/list/listvacantland.txt','retrain/vacantland/dataset/annotations/list.txt'],
                     ['detected_object/output_data/list/trainvacantland.txt','retrain/vacantland/dataset/annotations/train.txt'],
                     ['detected_object/output_data/list/valvacantland.txt','retrain/vacantland/dataset/annotations/val.txt'],
                     ['detected_object/output_data/list/listsmoke.txt','retrain/smoke/dataset/annotations/list.txt'],
                     ['detected_object/output_data/list/trainsmoke.txt','retrain/smoke/dataset/annotations/train.txt'],
                     ['detected_object/output_data/list/valsmoke.txt','retrain/smoke/dataset/annotations/val.txt']]
    for src,dst in src_dist_list:
        _write_each_file(src,dst)
        