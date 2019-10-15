import os
import xml.etree.ElementTree as ET

files_path = "hxq_hxqzc"
xml_files = os.listdir(files_path)

for file in xml_files:
    print(file)
    if "xml" in file:
        tree = ET.parse(os.path.join(files_path, file))
        root = tree.getroot()
        for obj in root.findall('object'):
            if obj.find('name').text in ["hxq_yfps", "hxq_ywyc"]:
                obj.find('name').text = "hxq_yfyc"

        tree.write(os.path.join(files_path, file))


