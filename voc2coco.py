#!/usr/bin/python

# pip install lxml

import sys
import os
import json
import xml.etree.ElementTree as ET


START_BOUNDING_BOX_ID = 1
#PRE_DEFINE_CATEGORIES = {}
# If necessary, pre-define category and its id
PRE_DEFINE_CATEGORIES = {'knife':1,'scissors':2,'lighter':3,'zippooil':4,'pressure':5,
                            'slingshot':6,'handcuffs':7,'nailpolish':8,'powerbank':9,'firecrackers':10}

xml_list = []
file_list = []
def get_list(path):
    for x in os.listdir(path):
        if x.split('.')[-1] == 'xml':
            xml_list.append(os.path.join(path,x))
        else:
            get_list(oa.path.join(path,x))

def get(root, name):
    vars = root.findall(name)
    return vars


def get_and_check(root, name, length):
    vars = root.findall(name)
    if len(vars) == 0:
        raise NotImplementedError('Can not find %s in %s.'%(name, root.tag))
    if length > 0 and len(vars) != length:
        raise NotImplementedError('The size of %s is supposed to be %d, but is %d.'%(name, length, len(vars)))
    if length == 1:
        vars = vars[0]
    return vars


def get_filename_as_int(filename):
    try:
        filename = filename.split('/')[-1][:-4]
        return int(filename)
    except:
        raise NotImplementedError('Filename %s is supposed to be an integer.'%(filename))


def convert(json_file):
    #list_fp = open(xml_list, 'r')
    json_dict = []
    categories = PRE_DEFINE_CATEGORIES
    bnd_id = START_BOUNDING_BOX_ID
    for xml_f in xml_list:
        print("Processing %s"%(xml_f))
        tree = ET.parse(xml_f)
        root = tree.getroot()
        path = get(root, 'path')

        filename = root.find('filename').text.split('/')[-1]
        

        for obj in get(root, 'object'):
            category = get_and_check(obj, 'name', 1).text
            bndbox = get_and_check(obj, 'bndbox', 1)
            xmin = float(get_and_check(bndbox, 'xmin', 1).text)
            ymin = float(get_and_check(bndbox, 'ymin', 1).text)
            xmax = float(get_and_check(bndbox, 'xmax', 1).text)
            ymax = float(get_and_check(bndbox, 'ymax', 1).text)
            assert(xmax > xmin)
            assert(ymax > ymin)
            o_width = abs(xmax - xmin)
            o_height = abs(ymax - ymin)
            ann = {'name': filename, 'detect_name':
                   category, 'bbox':[xmin, ymin, o_width, o_height]}
            json_dict.append(ann)

    json_fp = open(json_file, 'w')
    json_str = json.dumps(json_dict)
    json_fp.write(json_str)
    json_fp.close()
    

if __name__ == '__main__':
    path = './Annotations'
    get_list(path)

    convert('./coco.json')
