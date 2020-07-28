import os
import numpy as np
import codecs
import json
from glob import glob
import cv2
import shutil
from sklearn.model_selection import train_test_split
from tqdm import tqdm
import pandas as pd
import pdb

w_h = []
w = []
h = []
labels = []
json_file  = "./Duck_inject_normalv2.json"
files = [1]

#4.读取标注信息并写入 xml
for tmp in files:
    json_filename = json_file
    anno_result = pd.read_json(open(json_filename,"r",encoding="utf-8"))
    
    name_list=anno_result["name"].unique()
    for img_name in name_list:
            img_anno = anno_result[anno_result["name"] == img_name]
            bboxs = img_anno["bbox"].tolist()
            detect_names = img_anno["detect_name"].tolist()
            assert img_anno["name"].unique()[0] == img_name
            #print(img_name,bboxs,detect_names)
            with codecs.open("./Annotations/" + img_name.split('.')[0] + ".xml","w","utf-8") as xml:
                img_path = './JPEGImages/'+img_name
                img = cv2.imread(img_path)
                #pdb.set_trace()
                height, width, channels = img.shape[0],img.shape[1],img.shape[2]

                xml.write('<annotation>\n')
                xml.write('\t<folder>' + 'UAV_data' + '</folder>\n')
                xml.write('\t<filename>' + img_name + '</filename>\n')
                xml.write('\t<size>\n')
                xml.write('\t\t<width>'+ str(width) + '</width>\n')
                xml.write('\t\t<height>'+ str(height) + '</height>\n')
                xml.write('\t\t<depth>' + str(channels) + '</depth>\n')
                xml.write('\t</size>\n')
                xml.write('\t\t<segmented>0</segmented>\n')
                
                
                for bbox, detect_name in zip(bboxs, detect_names):
                    label= detect_name
                    points = np.array(bbox)
                    xmin = points[0]
                    xmax = points[2]
                    ymin = points[1]
                    ymax = points[3]
                    if xmax <= xmin or ymax <= ymin:
                        continue
                    else:
                        xml.write('\t<object>\n')
                        xml.write('\t\t<name>'+str(label)+'</name>\n')
                        xml.write('\t\t<pose>Unspecified</pose>\n')
                        xml.write('\t\t<truncated>1</truncated>\n')
                        xml.write('\t\t<difficult>0</difficult>\n')
                        xml.write('\t\t<bndbox>\n')
                        xml.write('\t\t\t<xmin>' + str(xmin) + '</xmin>\n')
                        xml.write('\t\t\t<ymin>' + str(ymin) + '</ymin>\n')
                        xml.write('\t\t\t<xmax>' + str(xmax) + '</xmax>\n')
                        xml.write('\t\t\t<ymax>' + str(ymax) + '</ymax>\n')
                        xml.write('\t\t</bndbox>\n')
                        xml.write('\t</object>\n')
                        w_h.append(max(int((xmax-xmin)/(ymax-ymin)),int((ymax-ymin)/(xmax-xmin))))
                        w.append(int(xmax-xmin))
                        h.append(int(ymax-ymin))
                        labels.append(label)
                    # print(multi['name'],xmin,ymin,xmax,ymax,label)
                xml.write('</annotation>')
        
# # 5.复制图片到 VOC2007/JPEGImages/下
# image_files = glob(image_path + "*.jpg")
# print("copy image files to VOC20/JPEGImages/")
# for image in tqdm(image_files):
#     shutil.copy(image,saved_path +"JPEGImages/")

w_h_list = list(set(w_h))
w_h_cnt = [w_h.count(x) for x in w_h_list]
w_list  = list(set(w))
w_cnt = [w.count(x) for x in w_list]
h_list  = list(set(h))
h_cnt = [h.count(x) for x in h_list]
labels_list = list(set(labels))
labels_cnt = [labels.count(x) for x in labels_list]

#6.split files for txt
txtsavepath = "./ImageSets/Main/"
ftrainval = open(txtsavepath+'/trainval.txt', 'w')
ftest = open(txtsavepath+'/test.txt', 'w')
ftrain = open(txtsavepath+'/train.txt', 'w')
fval = open(txtsavepath+'/val.txt', 'w')
total_files = os.listdir("./Annotations/")

total_files = [i.split("/")[-1].split(".xml")[0] for i in total_files]
#test_filepath = ""
for file in total_files:
    ftrainval.write(file + "\n")
    
#split
train_files,val_files = train_test_split(total_files,test_size=0.15,random_state=42)
#train
for file in train_files:
    ftrain.write(file + "\n")
#val
for file in val_files:
    fval.write(file + "\n")

ftrainval.close()
ftrain.close()
fval.close()
ftest.close()   
