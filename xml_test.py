import numpy as np
import cv2
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

CLASSES = ('hxq_gjbs', 'hxq_gjtps', 'hxq_gjzc', 'hxq_yfps', 'hxq_ywyc', 'hxq_yfzc')

# 读取图片
img = cv2.imread("28_hxq_yfps_1.jpg")

# 读取xml
tree = ET.parse('28_hxq_yfps_1.xml')
root = tree.getroot()
objs = root.findall('object')

i = 0
for index, obj in enumerate(objs):
    # 找到的hxq需要保留的object
    object_index = []
    if obj.find('name').text == 'hxq':
        # 记录hxq的index
        object_index.append(index)
        print("{}_hxq".format(str(i)) + ":"+ str(index))

        hxq_bnd_box = obj.find('bndbox')
        hxq_bbox = [
            int(hxq_bnd_box.find('xmin').text),
            int(hxq_bnd_box.find('ymin').text),
            int(hxq_bnd_box.find('xmax').text),
            int(hxq_bnd_box.find('ymax').text)
        ]
        # 截取hxq部分图像
        img_crop = img[hxq_bbox[1]: hxq_bbox[3], hxq_bbox[0]: hxq_bbox[2]]
        cv2.imwrite(str(i)+".jpg", img_crop)

        # 生成xml文件副本，便于后续处理
        tree_copy = ET.parse('28_hxq_yfps_1.xml')
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
                    bnd_box.find('xmax').text = str(min(bbox[2] - hxq_bbox[0], hxq_bbox_copy[2] - hxq_bbox_copy[0]))
                    bnd_box.find('ymax').text = str(min(bbox[3] - hxq_bbox[1], hxq_bbox_copy[3] - hxq_bbox_copy[1]))

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

        tree_copy.write('{}.xml'.format(str(i)))
        i = i + 1