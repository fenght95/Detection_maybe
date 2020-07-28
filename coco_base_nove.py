import json
import pdb

COCO_CLS = ('person', 'bicycle', 'car', 'motorcycle', 'airplane', 'bus',
               'train', 'truck', 'boat', 'traffic light', 'fire hydrant',
               'stop sign', 'parking meter', 'bench', 'bird', 'cat', 'dog',
               'horse', 'sheep', 'cow', 'elephant', 'bear', 'zebra', 'giraffe',
               'backpack', 'umbrella', 'handbag', 'tie', 'suitcase', 'frisbee',
               'skis', 'snowboard', 'sports ball', 'kite', 'baseball bat',
               'baseball glove', 'skateboard', 'surfboard', 'tennis racket',
               'bottle', 'wine glass', 'cup', 'fork', 'knife', 'spoon', 'bowl',
               'banana', 'apple', 'sandwich', 'orange', 'broccoli', 'carrot',
               'hot dog', 'pizza', 'donut', 'cake', 'chair', 'couch',
               'potted plant', 'bed', 'dining table', 'toilet', 'tv', 'laptop',
               'mouse', 'remote', 'keyboard', 'cell phone', 'microwave',
               'oven', 'toaster', 'sink', 'refrigerator', 'book', 'clock',
               'vase', 'scissors', 'teddy bear', 'hair drier', 'toothbrush')

VOC_CLS = ('airplane','bicycle','bird','boat','bottle','bus','car', 'cat',
             'chair','cow','dining table','dog','horse','motorcycle','person','potted plant','sheep',
             'couch', 'train', 'tv')


if __name__ == '__main__':
	print(len(VOC_CLS))
	print(len(COCO_CLS))
	BASE_CLS = [x for x in COCO_CLS if x not in VOC_CLS]
	
	json_files = ['./instances_train2017.json','./instances_val2017.json']
	for file in json_files:
		f = open(file,'r',encoding='utf-8')
		coco = json.load(f)
		f.close()
		
		new_coco = {} 
		new_coco['info'] = coco['info']
		new_coco['licenses'] = coco['licenses']
		new_coco['images'] = coco['images']
		new_coco['categories'] = []
		new_coco['annotations'] = []
		cats = coco['categories']
		ids = []
		#pdb.set_trace()
		print('all annotations len %d'%len(coco['annotations']))
		for cat in cats:
			if cat['name'] not in BASE_CLS:
				ids.append(cat['id'])
				new_coco['categories'].append(cat)
		#pdb.set_trace()
		print(len(new_coco['categories']),len(ids))
		for anno in coco['annotations']:
			if anno['category_id'] in ids:
				new_coco['annotations'].append(anno)
		data = json.dumps(new_coco)
		with open(file[:-5]+'_nove.json','w') as f:
			json.dump(new_coco,f)
		print('annotations len %d'%len(new_coco['annotations']))
