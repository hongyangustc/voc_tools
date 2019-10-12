import os
import cv2
import argparse
import xml.etree.ElementTree as ET

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='XML+JPG to image crops converter')
    parser.add_argument('dataset_path', type=str, help='Path to the VOC-format dataset')
    parser.add_argument('--output_path', type=str, default='data', help='Path to the output image path')
    args = parser.parse_args()

    xmls_path = args.dataset_path
    imgs_path = args.dataset_path
    xml_filenames = os.listdir(xmls_path)
    img_filenames = os.listdir(imgs_path)

    os.makedirs(os.path.join(args.output_path, 'jyz'), exist_ok=True)
    os.makedirs(os.path.join(args.output_path, 'jyz_pl'), exist_ok=True)
    os.makedirs(os.path.join(args.output_path, 'jyz_lw'), exist_ok=True)
    os.makedirs(os.path.join(args.output_path, 'jyz_zc'), exist_ok=True)

    count = 0
    for xml_filename in xml_filenames:
        if 'xml' in xml_filename:
            print('XML:', xml_filename)
            data = ET.parse(os.path.join(xmls_path, xml_filename))
            root = data.getroot()
            image = cv2.imread(os.path.join(imgs_path, xml_filename[:-3] + 'jpg'))

            for child in root.iter(tag='object'):
                name = child.iter(tag='name').__next__()
                box = child.iter(tag='bndbox').__next__()
                xmin = int(box.iter(tag='xmin').__next__().text)
                ymin = int(box.iter(tag='ymin').__next__().text)
                xmax = int(box.iter(tag='xmax').__next__().text)
                ymax = int(box.iter(tag='ymax').__next__().text)

                if 'jyz' in name.text:
                    crop = image[ymin: ymax, xmin: xmax]
                    if name.text == 'jyz' or name.text == 'jyz_pl' or name.text == 'jyz_lw' or name.text == 'jyz_zc':
                        print(name.text)
                        cv2.imwrite(os.path.join(os.path.join(args.output_path, name.text, '{}.jpg'.format(count))),
                                    crop)
                        cv2.imshow('crop', crop)
                        cv2.waitKey(1)
                    else:
                        print('Unexpected tag: ', name.text)
                    count += 1
