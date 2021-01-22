import os
from xml.etree import ElementTree
from xml.etree.ElementTree import Element, SubElement
from lxml import etree
import codecs

def write_xml(path,name):
    xml = codecs.open(os.path.join(path,name + '.xml'), 'w', encoding='utf-8')
    xml.write('<annotation>\n')
    xml.write('\t<folder>' + '' + '</folder>\n')
    xml.write('\t<filename>' + name + '</filename>\n')
    xml.write('\t<source>\n')
    xml.write('\t\t<database>Unknown</database>\n')
    xml.write('\t</source>\n')
    xml.write('\t<size>\n')
    xml.write('\t\t<width>' + str() + '</width>\n')
    xml.write('\t\t<height>' + str() + '</height>\n')
    xml.write('\t\t<depth>' + str(3) + '</depth>\n')
    xml.write('\t</size>\n')
    xml.write('\t\t<segmented>0</segmented>\n')
    xml.write('</annotation>')


names = os.listdir('')
xmls = os.listdir('')
for i in range(len(xmls)):
    xmls[i] = xmls[i].split('.')[0]
i = 1
for name in names:
    if name.split('.')[0] not in xmls:
        print(name.split('.')[0], i)
        i = i + 1
        write_xml('./xml_demo/xml',name.split('.')[0])
