import xml.etree.ElementTree as ET
import os
import cv2
import numpy as np
from matplotlib import pyplot as plt
import pdb

CLASSES = ('bus', 'bicycle', 'car', 'person', 'truck', 'tricycle')

def plot_hist(txt):
	if txt.split('.')[-1] == 'txt':
		with open(txt, 'r') as f:
			xmls = f.readlines()
	else:
		xmls = os.listdir(txt)
	areas = []
	ratio = []
	for xml in xmls:
		#img = cv2.imread('./xml_demo/rgb/' + xml + '.jpg')
		tree = ET.parse('./xml_demo/xml/' + xml)
		root = tree.getroot()
		for obj in root.findall('object'):
			name = obj.find('name').text
			bnd_box = obj.find('bndbox')
			x1,y1,x2,y2 = int(bnd_box.find('xmin').text),int(bnd_box.find('ymin').text),int(bnd_box.find('xmax').text),int(bnd_box.find('ymax').text)
			areas.append((x2-x1)*(y2-y1))
			if x2 == x1:
				print(xml)
				pdb.set_trace()
			ratio.append((y2-y1)/ (x2 - x1))
			#cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 1)
			#cv2.putText(img, name, (x1, y1), cv2.FONT_HERSHEY_SIMPLEX, 0.2, (0, 255, 0), 1)
		#cv2.imwrite('./369.jpg',img)


	square_array = np.array(areas)
	square_max = np.max(square_array)
	square_min = np.min(square_array)
	square_mean = np.mean(square_array)
	#square_var = np.var(square_array)
	plt.figure(1)
	plt.hist(square_array,25)
	#plt.xlabel('Area in pixel')
	#plt.ylabel('Frequency of area')
	#plt.title('Area' )
	print(square_max,square_min,square_mean)
	plt.savefig('areas.jpg')


	ratio_array = np.array(ratio)
	ratio_max = np.max(ratio_array)
	ratio_min = np.min(ratio_array)
	ratio_mean = np.mean(ratio_array)
	ratio_var = np.var(ratio_array)
	plt.figure(2)
	plt.hist(ratio_array,25)
	#plt.xlabel('Ratio of length / width')
	#plt.ylabel('Frequency of ratio')
	#plt.title('Ratio')
	plt.savefig('ratio.jpg')
	print(ratio_max,ratio_min,ratio_mean)
	#plt.show()

#plot_hist('./xml_demo/xml/')
#plot_hist('train_3.txt')
#plot_hist('test_random.txt')
#plot_hist('train_random.txt')

def plot_pie(txt):
	nums = {cat: 0 for cat in CLASSES}
	with open(txt, 'r') as f:
		xmls = f.readlines()
	for xml in xmls:
		tree = ET.parse('./xml_demo/xml/' + xml.strip() + '.xml')
		root = tree.getroot()
		for obj in root.findall('object'):
			name = obj.find('name').text
			if name not in CLASSES:
				print(xml, name)
			else:
				nums[name] = nums[name] + 1
	plt.figure()
	plt.pie(nums.values(),labels=nums.keys(),autopct='%1.2f%%')
	plt.savefig(txt.split('.')[0]+'.jpg')

#for txt in ['train_3.txt', 'test_3.txt', 'train_random.txt','test_random.txt']:
#	plot_pie(txt)

def plot_labels_hist(txt):
	if txt.split('.')[-1] == 'txt':
		with open(txt, 'r') as f:
			xmls = f.readlines()
	else:
		xmls = os.listdir(txt)
	nums = {cat: 0 for cat in CLASSES}
	for xml in xmls:
		tree = ET.parse('./xml_demo/xml/' + xml.strip())
		root = tree.getroot()
		for obj in root.findall('object'):
			name = obj.find('name').text
			nums[name] = nums[name] + 1



	plt.bar(nums.keys(),nums.values(),width=0.5)
	for i,j in zip(nums.keys(),nums.values()):
		plt.text(i,j+0.5,'%d'%j,ha = 'center',va = 'bottom')
	plt.show()


#plot_labels_hist('./xml_demo/xml')



def show_labels(txt):
	if isinstance(txt,str):
		xmls = os.listdir(txt)
	elif isinstance(txt,list):
		xmls = txt
	for xml in xmls:
		img = cv2.imread('./xml_demo/rgb/' + xml.split('.')[0].strip() + '.jpg')
		trm = cv2.imread('./xml_demo/trm/' + xml.split('.')[0].strip() + '.jpg')
		tree = ET.parse('./xml_demo/xml/' + xml.split('.')[0].strip() + '.xml')
		root = tree.getroot()
		for obj in root.findall('object'):
			name = obj.find('name').text
			bnd_box = obj.find('bndbox')
			x1,y1,x2,y2 = int(bnd_box.find('xmin').text),int(bnd_box.find('ymin').text),int(bnd_box.find('xmax').text),int(bnd_box.find('ymax').text)
			cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 1)
			cv2.putText(img, name, (x1, y1), cv2.FONT_HERSHEY_SIMPLEX, 0.2, (0, 255, 0), 1)
			cv2.rectangle(trm, (x1, y1), (x2, y2), (0, 255, 0), 1)
			cv2.putText(trm, name, (x1, y1), cv2.FONT_HERSHEY_SIMPLEX, 0.2, (0, 255, 0), 1)

		cv2.imwrite('./imshow_r/' + xml.split('.')[0].strip() + '.jpg',img)
		cv2.imwrite('./imshow_t/' + xml.split('.')[0].strip() + '.jpg', trm)

txt = ['2-1_Z__000667', 'DJI_20201120201339_0003_Z__000088',
            'DJI_20201121164229_0004_Z__000078',
            'DJI_20201121164530_0005_Z__000132',
            'DJI_20201121172753_0006_Z__000245',
            'DJI_20201121173104_0007_Z__000369']
show_labels(txt)

# day night split
# train 3650
# test 1900

# random split 8:2
# train 4400
# test 1100
