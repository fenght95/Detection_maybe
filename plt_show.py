import xml.etree.ElementTree as ET
import os
import cv2
import numpy as np
from matplotlib import pyplot as plt
import pdb

CLASSES = ()

def plot_hist(txt):
	if txt.split('.')[-1] == 'txt':
		with open(txt, 'r') as f:
			xmls = f.readlines()
	else:
		xmls = os.listdir(txt)
	areas = []
	ratio = []
	for xml in xmls:
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


	square_array = np.array(areas)
	square_max = np.max(square_array)
	square_min = np.min(square_array)
	square_mean = np.mean(square_array)
	plt.figure(1)
	plt.hist(square_array,25)
	print(square_max,square_min,square_mean)
	plt.savefig('areas.jpg')


	ratio_array = np.array(ratio)
	ratio_max = np.max(ratio_array)
	ratio_min = np.min(ratio_array)
	ratio_mean = np.mean(ratio_array)
	plt.figure(2)
	plt.hist(ratio_array,25)
	plt.savefig('ratio.jpg')
	print(ratio_max,ratio_min,ratio_mean)


#plot_hist('train_.txt')


def plot_pie(txt):
	nums = {cat: 0 for cat in CLASSES}
	with open(txt, 'r') as f:
		xmls = f.readlines()
	for xml in xmls:
		tree = ET.parse('' + xml.strip() + '.xml')
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

for txt in []:
	plot_pie(txt)

def plot_labels_hist(txt):
	if txt.split('.')[-1] == 'txt':
		with open(txt, 'r') as f:
			xmls = f.readlines()
	else:
		xmls = os.listdir(txt)
	nums = {cat: 0 for cat in CLASSES}
	for xml in xmls:
		tree = ET.parse( + xml.strip())
		root = tree.getroot()
		for obj in root.findall('object'):
			name = obj.find('name').text
			nums[name] = nums[name] + 1



	plt.bar(nums.keys(),nums.values(),width=0.5)
	for i,j in zip(nums.keys(),nums.values()):
		plt.text(i,j+0.5,'%d'%j,ha = 'center',va = 'bottom')
	plt.show()


plot_labels_hist('')



def show_labels(txt):
	if isinstance(txt,str):
		xmls = os.listdir(txt)
	elif isinstance(txt,list):
		xmls = txt
	for xml in xmls:
		img = cv2.imread('' + xml.split('.')[0].strip() + '.jpg')
		trm = cv2.imread('' + xml.split('.')[0].strip() + '.jpg')
		tree = ET.parse('' + xml.split('.')[0].strip() + '.xml')
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

txt = []
show_labels(txt)
