# -*- coding: utf-8 -*-
import zipfile
import xml.etree.ElementTree as ET
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

DOCX_PATH = r"d:\SoftData\Obsidian\JA-algorithm2\A算法模版.docx"

W_NS = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'

def find_drawing_elements(docx_path):
    with zipfile.ZipFile(docx_path, 'r') as z:
        with z.open('word/document.xml') as f:
            tree = ET.parse(f)
            root = tree.getroot()
            
            body = None
            for child in root:
                tag_local = child.tag.split('}')[1] if '}' in child.tag else child.tag
                if tag_local == 'body':
                    body = child
                    break
            
            if body is None:
                print("No body found!")
                return
            
            print("Searching for drawing elements in body children...")
            
            for idx, child in enumerate(body):
                tag_local = child.tag.split('}')[1] if '}' in child.tag else child.tag
                
                if tag_local == 'p':
                    for elem in child.iter():
                        elem_tag = elem.tag.split('}')[1] if '}' in elem.tag else elem_tag
                        if elem_tag == 'drawing':
                            print(f"\nFound drawing at body index {idx}!")
                            
                            for sub in elem.iter():
                                sub_tag = sub.tag.split('}')[1] if '}' in sub.tag else sub_tag
                                if sub_tag == 'txbxContent':
                                    print(f"  Found txbxContent!")
                                    break

if __name__ == '__main__':
    find_drawing_elements(DOCX_PATH)
