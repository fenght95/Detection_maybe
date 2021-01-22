import xml.etree.ElementTree as ET
import os
CLASSES = ('bus', 'bicycle', 'car', 'person', 'truck', 'tricycle')

nums = {cat:0 for cat in CLASSES}


xmls = os.listdir('./xml_demo/xml')
#with open('./test_v.txt','r') as f:
#    xmls = f.readlines()
for xml in xmls:
    tree = ET.parse('./xml_demo/xml/' + xml.strip())
    root = tree.getroot()
    for obj in root.findall('object'):
        name = obj.find('name').text
        if name not in CLASSES:
            print(xml, name)
        else:
            nums[name] = nums[name] + 1

# ALL
#{'bus': 2584, 'bicycle': 4060, 'car': 45449, 'person': 395, 'truck': 6194, 'tricycle': 19}
print(nums)