import xml.etree.ElementTree as ET
import os

nums = {cat:0 for cat in CLASSES}


xmls = os.listdir('')

for xml in xmls:
    tree = ET.parse( + xml.strip())
    root = tree.getroot()
    for obj in root.findall('object'):
        name = obj.find('name').text
        if name not in CLASSES:
            print(xml, name)
        else:
            nums[name] = nums[name] + 1

print(nums)
