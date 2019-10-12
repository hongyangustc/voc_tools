# -*- coding:utf-8 -*-
"""
功能：对自己制作的pascal voc图片和xml文件重命名
"""
import os
from PIL import Image
from PIL.ExifTags import TAGS


import xml.etree.ElementTree as Et


img_dir = 'JPEGImages'
xml_dir = 'Annotations'

files = os.listdir(xml_dir)

N = 0

for fi in files:
    xml_name = fi.split('.')[0] + '.xml'
    xml_newname = '{:0>6d}'.format(N) + '.xml'
    jpg_name = fi.split('.')[0] + '.jpg'
    jpg_newname = '{:0>6d}'.format(N) + '.jpg'

    xml_path = os.path.join(xml_dir, xml_name)
    xml_newpath = os.path.join(xml_dir, xml_newname)
    jpg_path = os.path.join(img_dir, jpg_name)
    jpg_newpath = os.path.join(img_dir, jpg_newname)
    # print(xml_name + "   " + xml_newname + "   " + jpg_name + "   " + jpg_newname)
    print(xml_path + "   " + xml_newpath + "   " + jpg_path + "   " + jpg_newpath)
    os.rename(xml_path, xml_newpath)
    os.rename(jpg_path, jpg_newpath)

    N += 1
    print(N)
    
    # try:
    #     img = Image.open(jpg_path)
    # except:
    #     print(jpg_path)
    #     continue
    #
    # ret = {}
    #
    # try:
    #     info = img._getexif()
    # except:
    #     continue
    #
    # if info == None:
    #     continue
    #
    # for tag, value in info.items():
    #     decoded = TAGS.get(tag, tag)
    #     ret[decoded] = value
    # orientation = ret.get('Orientation', None)
    #
    # if orientation not in ss:
    #     ss[orientation] = 1
    # else:
    #     ss[orientation] += 1
    #
    # if orientation not in name_dict:
    #     name_dict[orientation] = fi
    # if N>5000:
    #     break

# for key in ss:
#     print(key, ss[key])

# for key in name_dict:
#     print(key, name_dict[key])

# print(N)
    #print(N, fi, orientation)

