# -*- coding:utf-8 -*-
"""
截取原始voc数据中hxq部分，并修改xml文件
"""
import os
import cv2
import numpy as np
import argparse
import xml.etree.ElementTree as ET

# 计算iou
def calc_iou(bbox1, bbox2):
    if not isinstance(bbox1, np.ndarray):
        bbox1 = np.array(bbox1)
    if not isinstance(bbox2, np.ndarray):
        bbox2 = np.array(bbox2)
    xmin1, ymin1, xmax1, ymax1, = np.split(bbox1, 4, axis=-1)
    xmin2, ymin2, xmax2, ymax2, = np.split(bbox2, 4, axis=-1)

    area1 = (xmax1 - xmin1) * (ymax1 - ymin1)
    area2 = (xmax2 - xmin2) * (ymax2 - ymin2)

    ymin = np.maximum(ymin1, np.squeeze(ymin2, axis=-1))
    xmin = np.maximum(xmin1, np.squeeze(xmin2, axis=-1))
    ymax = np.minimum(ymax1, np.squeeze(ymax2, axis=-1))
    xmax = np.minimum(xmax1, np.squeeze(xmax2, axis=-1))

    h = np.maximum(ymax - ymin, 0)
    w = np.maximum(xmax - xmin, 0)
    intersect = h * w

    # union = area1 + np.squeeze(area2, axis=-1) - intersect
    # return intersect / union
    return intersect / area2

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='XML+JPG to image crops converter')
    parser.add_argument('--dataset_path', default='hxq', type=str, help='Path to the VOC-format dataset')
    parser.add_argument('--output_path', type=str, default='data', help='Path to the output image path')
    args = parser.parse_args()

    CLASSES = ('hxq_gjbs', 'hxq_gjtps', 'hxq_gjzc', 'hxq_yfps', 'hxq_ywyc', 'hxq_yfzc')

    xmls_path = args.dataset_path
    imgs_path = args.dataset_path
    xml_filenames = os.listdir(xmls_path)
    img_filenames = os.listdir(imgs_path)

    voc_dir = os.path.join(args.output_path, 'VOCdevkit')
    voc_07dir = os.path.join(args.output_path, 'VOCdevkit/VOC2007')
    voc_xmldir = os.path.join(args.output_path, 'VOCdevkit/VOC2007/Annotations')
    voc_imgdir = os.path.join(args.output_path, 'VOCdevkit/VOC2007/JPEGImages')
    voc_txtdir = os.path.join(args.output_path, 'VOCdevkit/VOC2007/ImageSets/Main')


    os.makedirs(voc_dir, exist_ok=True)
    os.makedirs(voc_07dir, exist_ok=True)
    os.makedirs(voc_xmldir, exist_ok=True)
    # os.makedirs(voc_txtdir[:len(voc_txtdir.split("/")[-1])], exist_ok=True)
    # os.makedirs(voc_txtdir.replace(voc_txtdir.split("/")[-1], ''), exist_ok=True)
    os.makedirs(voc_txtdir.rsplit("/")[0], exist_ok=True)
    os.makedirs(voc_txtdir, exist_ok=True)
    os.makedirs(voc_imgdir, exist_ok=True)

    count = 0
    for xml_filename in xml_filenames:
        if 'xml' in xml_filename:
            print('XML:', xml_filename)

            # 读取图片
            img = cv2.imread(os.path.join(imgs_path, xml_filename[:-3] + 'jpg'))
            # 读取xml
            tree = ET.parse(os.path.join(xmls_path, xml_filename))
            root = tree.getroot()
            objs = root.findall('object')

            # i = 0
            for index, obj in enumerate(objs):
                # 找到的hxq需要保留的object
                object_index = []
                if obj.find('name').text == 'hxq':
                    # 记录hxq的index
                    object_index.append(index)
                    # print("{}_hxq".format(str(i)) + ":" + str(index))

                    hxq_bnd_box = obj.find('bndbox')
                    hxq_bbox = [
                        int(hxq_bnd_box.find('xmin').text),
                        int(hxq_bnd_box.find('ymin').text),
                        int(hxq_bnd_box.find('xmax').text),
                        int(hxq_bnd_box.find('ymax').text)
                    ]
                    # 截取hxq部分图像
                    img_crop = img[hxq_bbox[1]: hxq_bbox[3], hxq_bbox[0]: hxq_bbox[2]]
                    cv2.imwrite(os.path.join(voc_imgdir, '{:0>6d}.jpg'.format(count)), img_crop)
                    # 生成xml文件副本，便于后续处理
                    tree_copy = ET.parse(os.path.join(xmls_path, xml_filename))
                    root_copy = tree_copy.getroot()
                    objs_copy = root_copy.findall('object')

                    # 修改hxq矩形框值
                    hxq_bnd_box_copy = objs_copy[index].find('bndbox')
                    hxq_bbox_copy = [
                        int(hxq_bnd_box_copy.find('xmin').text),
                        int(hxq_bnd_box_copy.find('ymin').text),
                        int(hxq_bnd_box_copy.find('xmax').text),
                        int(hxq_bnd_box_copy.find('ymax').text)
                    ]
                    hxq_bnd_box_copy.find('xmin').text = str(0)
                    hxq_bnd_box_copy.find('ymin').text = str(0)
                    hxq_bnd_box_copy.find('xmax').text = str(hxq_bbox_copy[2] - hxq_bbox_copy[0])
                    hxq_bnd_box_copy.find('ymax').text = str(hxq_bbox_copy[3] - hxq_bbox_copy[1])

                    for index_copy, obj_copy in enumerate(objs_copy):
                        if obj_copy.find('name').text in CLASSES:
                            bnd_box = obj_copy.find('bndbox')
                            bbox = [
                                int(bnd_box.find('xmin').text),
                                int(bnd_box.find('ymin').text),
                                int(bnd_box.find('xmax').text),
                                int(bnd_box.find('ymax').text)
                            ]
                            # 判断硅胶或者油封属于哪个hxq
                            iou = calc_iou(hxq_bbox, bbox)
                            if iou > 0.8:
                                # 修改本hxq内的硅胶或者油封的矩形框
                                bnd_box.find('xmin').text = str(max(bbox[0] - hxq_bbox[0], 0))
                                bnd_box.find('ymin').text = str(max(bbox[1] - hxq_bbox[1], 0))
                                bnd_box.find('xmax').text = str(
                                    min(bbox[2] - hxq_bbox[0], hxq_bbox_copy[2] - hxq_bbox_copy[0]))
                                bnd_box.find('ymax').text = str(
                                    min(bbox[3] - hxq_bbox[1], hxq_bbox_copy[3] - hxq_bbox_copy[1]))

                                # 保存在这个hxq中油封或者硅胶的index
                                object_index.append(index_copy)
                            else:
                                continue
                    # 剔除不在这个hxq中的部分
                    for num in range(len(objs_copy)):
                        if num not in object_index:
                            root_copy.remove(objs_copy[num])
                        else:
                            continue

                    tree_copy.write(os.path.join(voc_xmldir, '{:0>6d}.xml'.format(count)))
                    count += 1
                    # i = i + 1


    print("hxq_all_num:", count)
    #