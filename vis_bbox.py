import cv2
import json
img_root = './normal_aug'
ann_file = './Duck_inject_normal.json'
name2label = {}

anno_result = pd.read_json(ann_file,'r')
name_list = anno_result['name'].unique()

result = []

for img in os.listdir(img_root):
	img_anno = anno_result[anno_result['name'] == img]
	bboxes = img_anno['bbox'].tolist()
	names = img_anno['detect_name'].tolist()
	test_img = cv2.imread(img_root+'/'+img)
	for idx in range(len(bboxes)):
		pts = bboxes[idx]
		xmin,ymin,xmax,ymax = pts[0],pts[1],pts[2],pts[3]
		cv2.putText(testimg, str(names[idx]),(int(xmin),int(ymin)),cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 3)
		cv2.rectangle(testimg, (int(xmin),int(ymin)), (int(xmax),int(ymax)), (0,0,255), 2)

	cv2.namedWindow("testimg",0);
    cv2.resizeWindow("testimg", 1200, 800);
    cv2.imshow('testimg',testimg)
    cv2.waitKey(0)
