import os
from PIL import Image
from PIL.ExifTags import TAGS


import xml.etree.ElementTree as Et


img_dir = 'JPEGImages'
xml_dir = 'Annotations'

files = os.listdir(xml_dir)

N = 0

ss = {}

name_dict = {}

for fi in files:
    N += 1
    xml_name = fi.split('.')[0] + '.xml'
    jpg_name = fi.split('.')[0] + '.jpg'
    
    xml_path = os.path.join(xml_dir, xml_name)
    jpg_path = os.path.join(img_dir, jpg_name)
    
    try:
        img = Image.open(jpg_path)
    except:
        print(jpg_path)
        continue

    ret = {}
    
    try:
        info = img._getexif()
    except:
        continue

    if info == None:
        continue

    for tag, value in info.items():
        decoded = TAGS.get(tag, tag)
        ret[decoded] = value
    orientation = ret.get('Orientation', None)
    
    if orientation not in ss:
        ss[orientation] = 1
    else:
        ss[orientation] += 1

    if orientation not in name_dict:
        name_dict[orientation] = fi
    if N>5000:
        break

for key in ss:
    print(key, ss[key])

for key in name_dict:
    print(key, name_dict[key])

print(N)
    #print(N, fi, orientation)
     
