# coding: utf-8
import time
from datetime import datetime # Current date time in local system print(datetime.now())
import xml.etree.cElementTree as ET

WAIT_TIME = 5
ENTRY_NUM = 5
FILENAME_TEMPLATE = "exp"
TABLE_NAME = "locations"
PATH = "C:/Users/timof/Documents/Programming/DataBases/LabsDB/Lab08/Exchange/"

current_entry = 0
while(True):
    filename = "{}{}_{}_{}.xml".format(PATH, FILENAME_TEMPLATE, TABLE_NAME, 
    str(datetime.now()).replace('.', '_').replace(':', '-').replace(' ', '_'))
    root = ET.Element("root")
    for i in range(current_entry, current_entry + ENTRY_NUM):
        doc = ET.SubElement(root, "doc")
        ET.SubElement(doc, "loc_num").text = "Город" + str(i)
        ET.SubElement(doc, "parent").text = "Россия"
    current_entry += ENTRY_NUM
    tree = ET.ElementTree(root)
    tree.write(filename)
    time.sleep(WAIT_TIME) # In seconds