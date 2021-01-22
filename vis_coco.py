import cv2
import json
import pandas as pd
import os

img_root = 'C:/Users/feng/Desktop/normal'
ann_file = 'C:/Users/feng/Desktop/Duck_inject_normalv2.json'
name2label = {}

anno_result = pd.read_json(ann_file,'r')
name_list = anno_result['name'].unique()

for img in os.listdir(img_root):
    img_anno = anno_result[anno_result['name'] == img]
    bboxes = img_anno['bbox'].tolist()
    names = img_anno['detect_name'].tolist()
    test_img = cv2.imread(img_root+'/'+img)
    for idx in range(len(bboxes)):
        pts = bboxes[idx]
        xmin,ymin,xmax,ymax = pts[0],pts[1],pts[2],pts[3]
        cv2.putText(test_img, str(names[idx]),(int(xmin),int(ymin)),cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255))
        cv2.rectangle(test_img, (int(xmin),int(ymin)), (int(xmax),int(ymax)), (0,0,255))

    cv2.namedWindow("testimg",0)
    cv2.resizeWindow("testimg", 1200, 800)
    cv2.imshow('testimg',test_img)
    cv2.waitKey(0)