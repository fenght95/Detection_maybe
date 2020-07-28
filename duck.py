import os
import json
import numpy as np
import pandas as pd
import cv2
import glob
import random
from PIL import Image
import time
from sklearn import metrics as mr
import pdb
import tqdm

random.seed(2019)

aug_name=['knife', 'scissors', 'nailpolish', 'zippooil','slingshot','lighter','pressure','handcuffs','powerbank','firecrackers']

root='./normal_aug'

save_dir='./normal/'
if not os.path.exists(save_dir):
    os.mkdir(save_dir)
# normal_img_root='./normal_images/'
# aug_dir='./normal_images_aug/'
anno_file='./Duck_inject_normal.json'
anno_result= pd.read_json(open(anno_file,"r"))
name_list=anno_result["name"].unique()

ring_width=10# default is 5

result=[]
last_result_length=0
img_name_count=0
for path in os.listdir(root):
    img_name=path
    #
    img_anno = anno_result[anno_result["name"] == img_name]
    bboxs = img_anno["bbox"].tolist()
    if bboxs == []:
        print(path)
    #pdb.set_trace()
    img_name_count+=1
    detect_names = img_anno["detect_name"].tolist()
    # defect_names = [defect_name2label[x] for x in defect_names]
    #print(detect_names)
    assert img_anno["name"].unique()[0] == img_name
    # testimg=cv2.imread(root+path+'/'+img_name)
    testimg=Image.open(root+'/'+path)
    template_img_name=path
    # temp_img=cv2.imread(root+path+'/'+template_img_name)
    temp_img=Image.open(root+'/'+template_img_name)
    save_temp_name='template_'+str(img_name_count)+'.jpg'
    bboxs_np = np.array(bboxs)
    all_xmin,all_ymin,all_w,all_h = bboxs_np[:,0],bboxs_np[:,1],bboxs_np[:,2],bboxs_np[:,3]
    all_xmax = all_xmin + all_w
    all_ymax = all_ymin + all_h
    for idx in range(len(bboxs)):
        pts=bboxs[idx]
        d_name=detect_names[idx]
        xmin=pts[0]
        ymin=pts[1]
        xmax=pts[2] 
        ymax=pts[3] 
        #pdb.set_trace()
        defect_w=pts[2] - xmin 
        defect_h=pts[3] - ymin
        #w_h=round(defect_w/defect_h,2)
        #h_w=round(defect_h/defect_w,2)
        # cv2.putText(testimg, str(d_name),(int(xmin),int(ymin)),cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 3)
        # 用于长条判断
        # print('w_h',w_h)
        # print('h_w',h_w)
        # print('defect_size:',(ymax-ymin)*(xmax-xmin))
        # cv2.putText(testimg, str(w_h),(int(xmin+10),int(ymin)),cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 3)
        # cv2.putText(testimg, str(h_w),(int(xmin+30),int(ymin)),cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 3)
        # cv2.rectangle(testimg, (int(xmin),int(ymin)), (int(xmax),int(ymax)), (0,0,255), 2)
        # 筛选长条的采点位置
        if int(testimg.size[1] - int(defect_h)) < 0:
        	pdb.set_trace()
        scale=0.2
        left_top_x=random.randint(1,int(testimg.size[0] - int(defect_w*scale)))
        left_top_y=random.randint(1,int(testimg.size[1] - int(defect_h*scale)))
        
        #print(defect_w,defect_h)
        for i in range(len(bboxs)):
        	if left_top_x >= all_xmin[i] and left_top_x <= all_xmax[i] or (left_top_y >= all_ymin[i] and left_top_y <= all_ymax[i]):
        		i = 0
        		left_top_x=random.randint(1,int(testimg.size[0] - int(defect_w*scale)))
        		left_top_y=random.randint(1,int(testimg.size[1] - int(defect_h*scale)))
        
        # print(left_top_x,left_top_y)
        mask=np.zeros_like(temp_img)
        if d_name in aug_name:
            mask[int(scale*(left_top_y-ring_width)):int(scale*(left_top_y+defect_h+ring_width)),int(scale*(left_top_x-ring_width)):int(scale*(left_top_x+defect_w+ring_width))]=255
            mask[int(left_top_y):int(scale*(left_top_y+defect_w)),int(left_top_x):int(scale*(left_top_x+defect_h))]=0

            # cv2.namedWindow("mask",0);
            # cv2.resizeWindow("mask", 1200, 800);
            # cv2.imshow('mask',mask)
            # cv2.imwrite('mask.jpg',mask)
            # cv2.waitKey(0)
            patch=testimg.crop((xmin,ymin,xmax,ymax))
            #====相似度计算==============================================================================================#
            patch1=patch.copy()
            patch2=temp_img.crop((left_top_x,left_top_y,int(left_top_x+patch1.size[0]),int(left_top_y+patch1.size[1])))

            # print('bbox:',(left_top_x,left_top_y,int(left_top_x+(xmax-xmin)),int(left_top_y+(ymax-ymin))))
            # print(patch1.size[0],patch1.size[1])
            # print(patch1.size,patch2.size)
            patch2.resize((patch1.size[0],patch1.size[1]))
            patch1=np.resize(patch1,-1)
            patch2=np.resize(patch2,-1)
            # print(patch1.shape)
            # print(patch2.shape)
            mutual_infor=mr.mutual_info_score(patch1,patch2)
            #print(mutual_infor)
            #==================================================================================================#
            if mutual_infor>0.8:
                #print(patch.size)
                patch=patch.resize((int(patch.size[0]*scale),int(patch.size[1]*scale)))
                #print(patch.size)
                temp_img.paste(patch,(left_top_x,left_top_y))
                temp_img = cv2.cvtColor(np.asarray(temp_img),cv2.COLOR_RGB2BGR)
                temp_img = cv2.inpaint(temp_img,mask[:,:,0],3,cv2.INPAINT_TELEA)
                temp_img = Image.fromarray(cv2.cvtColor(temp_img,cv2.COLOR_BGR2RGB))
                result.append({'name': save_temp_name, 'detect_name': d_name, 'bbox': [left_top_x,left_top_y,left_top_x+defect_w*scale,left_top_y+defect_h*scale]})
                result.append({'name':save_temp_name,'detect_name':d_name,'bbox':[xmin,ymin,xmax,ymax]})
            else:
                result.append({'name':save_temp_name,'detect_name':d_name,'bbox':[xmin,ymin,xmax,ymax]})
                continue
        else:  
            mask[int(left_top_y-ring_width):int(left_top_y+defect_h+ring_width),int(left_top_x-ring_width):int(left_top_x+defect_w+ring_width)]=255
            mask[int(left_top_y):int(left_top_y+defect_h),int(left_top_x):int(left_top_x+defect_w)]=0
            
            # cv2.namedWindow("mask",0);
            # cv2.resizeWindow("mask", 1200, 800);
            # cv2.imshow('mask',mask)
            # cv2.imwrite('mask.jpg',mask)
            # cv2.waitKey(0)
            patch=testimg.crop((xmin,ymin,xmax,ymax))
            #====相似度计算==============================================================================================#
            patch1=patch.copy()
            patch2=temp_img.crop((left_top_x,left_top_y,int(left_top_x+patch1.size[0]),int(left_top_y+patch1.size[1])))

            # print('bbox:',(left_top_x,left_top_y,int(left_top_x+(xmax-xmin)),int(left_top_y+(ymax-ymin))))
            # print(patch1.size[0],patch1.size[1])
            # print(patch1.size,patch2.size)
            patch2.resize((patch1.size[0],patch1.size[1]))
            patch1=np.resize(patch1,-1)
            patch2=np.resize(patch2,-1)
            # print(patch1.shape)
            # print(patch2.shape)
            mutual_infor=mr.mutual_info_score(patch1,patch2)
            #print(mutual_infor)
            #==================================================================================================#
            #print(save_temp_name)
            if mutual_infor>0.8:
                temp_img.paste(patch,(left_top_x,left_top_y))
                temp_img = cv2.cvtColor(np.asarray(temp_img),cv2.COLOR_RGB2BGR)
                temp_img = cv2.inpaint(temp_img,mask[:,:,0],3,cv2.INPAINT_TELEA)
                temp_img = Image.fromarray(cv2.cvtColor(temp_img,cv2.COLOR_BGR2RGB))
                result.append({'name': save_temp_name, 'detect_name': d_name, 'bbox': [left_top_x,left_top_y,left_top_x+defect_w,left_top_y+defect_h]})
                result.append({'name':save_temp_name,'detect_name':d_name,'bbox':[xmin,ymin,xmax,ymax]})
            else:
                result.append({'name':save_temp_name,'detect_name':d_name,'bbox':[xmin,ymin,xmax,ymax]})
                continue
     
            # cv2.rectangle(temp_img, (int(left_top_x),int(left_top_y)), (int(left_top_x+defect_h),int(left_top_y+defect_w)), (0,0,255), 2)
    temp_img.save(save_dir+save_temp_name)

    #test path
    json_name='./Duck_inject_normalv2.json'
    with open(json_name,'w') as fp:
        json.dump(result, fp, indent = 4, separators=(',', ': ')) 
    #print(img_name_count)




# json_name='./Duck_inject_normal.json'
# with open(json_name,'w') as fp:
#         json.dump(result, fp, indent = 4, separators=(',', ': '))            
        # testimg.show()
        # temp_img.show()
        # # sys.pause(0)
        # time.sleep(2)
        # print(defect_img_root+defect_name[1]+'/'+defect_name[1]+'.jpg')
        # cv2.namedWindow("testimg",0);
        # cv2.resizeWindow("testimg", 1200, 800);
        # cv2.imshow('testimg',testimg)

        # cv2.namedWindow("temp_img",0);
        # cv2.resizeWindow("temp_img", 1200, 800);
        # cv2.imshow('temp_img',temp_img)
        # cv2.waitKey(0)
# print(defect_name)
# testimg=cv2.imread(defect_img_root+defect_name[1]+'/'+defect_name[1]+'.jpg')
# print(defect_img_root+defect_name[1]+'/'+defect_name[1]+'.jpg')
# cv2.imshow('testimg',testimg)
# cv2.waitKey(0)
