"""
功能：根据xml分割出需要类的图片，并存入对应的文件夹
"""
import os
import cv2
import argparse
import xml.etree.ElementTree as ET

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='XML+JPG to image crops converter')
    parser.add_argument('--dataset_path', type=str, default='hxq', help='Path to the VOC-format dataset')
    parser.add_argument('--output_path', type=str, default='data', help='Path to the output image path')
    args = parser.parse_args()

    xmls_path = args.dataset_path
    imgs_path = args.dataset_path
    xml_filenames = os.listdir(xmls_path)
    img_filenames = os.listdir(imgs_path)
    CLASSES = ('hxq', 'hxq_gjbs', 'hxq_gjtps', 'hxq_gjzc', 'hxq_yfps', 'hxq_ywyc', 'hxq_yfzc')
    for cat in CLASSES:
        os.makedirs(os.path.join(args.output_path, cat), exist_ok=True)

        count = 0
        for xml_filename in xml_filenames:
            if 'xml' in xml_filename:
                print('XML:', xml_filename)
                data = ET.parse(os.path.join(xmls_path, xml_filename))
                root = data.getroot()


                for child in root.iter(tag='object'):
                    name = child.iter(tag='name').__next__()
                    box = child.iter(tag='bndbox').__next__()
                    xmin = int(box.iter(tag='xmin').__next__().text)
                    ymin = int(box.iter(tag='ymin').__next__().text)
                    xmax = int(box.iter(tag='xmax').__next__().text)
                    ymax = int(box.iter(tag='ymax').__next__().text)

                    if cat in name.text:
                        image = cv2.imread(os.path.join(imgs_path, xml_filename[:-3] + 'jpg'))
                        crop = image[ymin: ymax, xmin: xmax]
                        cv2.imwrite(os.path.join(os.path.join(args.output_path, name.text, '{:0>6d}.jpg'.format(count))), crop)
                        count += 1